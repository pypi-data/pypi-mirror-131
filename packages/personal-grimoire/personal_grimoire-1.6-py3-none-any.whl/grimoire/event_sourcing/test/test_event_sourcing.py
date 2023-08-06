from __future__ import annotations

import unittest

import pytest
import redis
from loguru import logger as logging
from pydantic import BaseModel

from grimoire.config import config
from grimoire.event_sourcing.message import MessageBroker


@pytest.mark.skipif(
    True,
    reason="need to create a separate testing location for each stream",
)
class EventSourcingTestCase(unittest.TestCase):
    data = [
        {"value": 55, "type": "deposit", "account": "jean"},
        {"value": 35, "type": "withdraw", "account": "jean"},
        {"value": 50, "type": "deposit", "account": "rhea"},
    ]
    topic_name = "test_bank"

    def test_balance_with_replay(self):
        account = "gandalf"
        writer = AccountWriter()
        writer.reset_account(account)
        message = MessageBroker("test_money_sum", storage_location="/tmp")

        message.register_consumer(writer.handle_balance_change)
        message.produce({"value": 55, "type": "deposit", "account": account})
        self.assertEqual(AccountBalance().get_balance(account), 55)
        message.produce({"value": 35, "type": "withdraw", "account": account})
        self.assertEqual(AccountBalance().get_balance(account), 20)

        writer.reset_account(account)
        message.replay()
        self.assertEqual(AccountBalance().get_balance(account), 20)

    def test_save_dict_and_load_in_next_run(self):
        MessageBroker(self.topic_name).produce(self.data[0])
        result = MessageBroker(self.topic_name).consume_last()

        self.assertEqual(result["value"], self.data[0]["value"])
        self.assertEqual(result["type"], self.data[0]["type"])
        self.assertEqual(result["account"], self.data[0]["account"])
        self.assertTrue("generated_date" in result)

    def test_write_to_redis(self):
        AccountWriter().set_value("jean", 10)
        self.assertEqual(AccountBalance().get_balance("jean"), 10)

    def test_play_history_on_join(self):
        account = "saruman"
        message = MessageBroker("test_play_history_on_join", storage_location="/tmp")

        message.produce({"account": account, "value": 99, "type": "deposit"})
        message.produce({"account": account, "value": 33, "type": "withdraw"})

        writer = AccountWriter()
        writer.reset_account(account)
        message.register_consumer(writer.handle_balance_change, catchup_on_history=True)
        self.assertEqual(AccountBalance().get_balance(account), 66)
        message.produce({"account": account, "value": 20, "type": "deposit"})
        self.assertEqual(AccountBalance().get_balance(account), 86)


def get_redis():
    return redis.Redis(
        host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True
    )


class Transaction(BaseModel):
    value: float
    type: str
    account: str


class AccountBalance:
    def get_balance(self, user: str):
        result = get_redis().hget(f"account:{user}", "account_balance")
        if not result:
            return 0

        return int(result)


class AccountWriter:
    # writes to redis the state of the operations
    def handle_balance_change(self, event):
        previous_balance = AccountBalance().get_balance(event["account"])

        if event["type"] == "deposit":
            balance = previous_balance + event["value"]
        else:
            balance = previous_balance - event["value"]

        account_key = f"account:{event['account']}"
        logging.debug(f"Account key: {account_key}")
        logging.debug(f"Previous balance: {previous_balance}")
        logging.debug(f"Current balance : {balance}")
        self.set_value(event["account"], balance)

    def reset_account(self, account):
        self.set_value(account, 0)

    def set_value(self, account, value):
        r = get_redis()
        r.hset(f"account:{account}", "account_balance", value)
