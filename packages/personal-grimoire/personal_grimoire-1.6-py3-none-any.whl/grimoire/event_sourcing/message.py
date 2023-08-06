import json
import logging
from typing import Optional
from uuid import uuid4

from grimoire.file import append_file_creating, file_exists, file_get_content
from grimoire.shell import shell
from grimoire.time import Date

DEFAULT_STORAGE_LOCATION: str = "/data/grimoire/message_topics"


class MessageBroker:
    # the default place to save the files
    topic_name: str
    # file location = storage_location + [optional namespace] + topic_name
    # file_location: str

    def __init__(
        self,
        topic_name: Optional[str] = None,
        storage_location: Optional[str] = None,
        namespace="",
    ):
        self.topic_name = topic_name if topic_name else ""
        self.namespace = namespace
        self.storage_location = (
            storage_location if storage_location else DEFAULT_STORAGE_LOCATION
        )

        self.consumer = None

    def produce(self, message: dict, topic_name: Optional[str] = None):
        self.topic_name = topic_name if topic_name else self.topic_name

        metadata = {"generated_date": Date.now_str(), "uuid": str(uuid4())}
        message = {**metadata, **message}
        self._append_file(self.file_location, json.dumps(message) + "\n")
        self._consumers_process_message(message)

    def register_consumer(self, consumer, catchup_on_history=False):
        """Adds a consumer and optionally catchup on history"""
        self.consumer = consumer
        if catchup_on_history:
            self.replay()

    def replay(self):
        logging.info("Replaying history")
        if not file_exists(self.file_location):
            logging.info(f"No history to replay in {self.file_location}")
            return

        messages = file_get_content(self.file_location)
        for message in messages:
            message = json.loads(message)
            self._consumers_process_message(message)

    def consume_last(self, topic_name: Optional[str] = None) -> Optional[dict]:
        self.topic_name = topic_name if topic_name else self.topic_name

        last_content = shell.run_with_result(
            f'tail -n100 "{self.file_location}" | grep -v "repeat last run" | tail -n 1'
        )

        decoded = json.loads(last_content)

        return decoded

    def _consumers_process_message(self, message):
        if self.consumer:
            self.consumer(message)

    @property
    def file_location(self):
        return f"{self.storage_location}/{self.namespace}/{self.topic_name}"

    def _append_file(self, file_name, content):
        logging.info(f"Appending to message file: {file_name}, content: {content}")
        return append_file_creating(file_name, content)
