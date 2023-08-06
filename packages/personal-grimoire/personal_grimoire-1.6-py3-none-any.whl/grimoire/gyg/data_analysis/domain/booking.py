import logging
from typing import Optional

from grimoire.gyg.data_analysis.domain.data_information import Info
from grimoire.gyg.data_analysis.utils import BaseAnalysis
from grimoire.time import Date


class Bookings(BaseAnalysis):
    def __init__(self, spark):
        self.spark = spark

    def bookings_trend(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ):
        """
        Returns the amount of money made through bookings by day in a given period

        """

        if not date_from:
            date_from = Date.parse_str("last week")
        if not date_to:
            date_to = Date.yesterday_str()

        logging.info(f"Date from: {date_from}")

        final_query = f"""
            select
                    sum({Info.booking_table}.adult_selling_price_eur) as money_sum,
                    FIRST(DATE({Info.booking_table}.date_of_checkout)) as day
                from {Info.booking_table}
                where DATE(date_of_checkout)<"{date_to}" and DATE(date_of_checkout)>"{date_from}"
                group by DAY(date_of_checkout)
                order by day asc

        """
        logging.info(final_query)

        df = self.spark.sql(final_query)

        return df

    def get_one(self):
        """
        Example of usage:
        grimoire gyg dbconnect get_a_booking | jLast
        """
        return self.spark.table(Info.booking_table).limit(1).toJSON().first()

    def total_tour_bookings(self, use_production: bool = False) -> str:
        query: str = f"""
            select b.tour_id, count(b.tour_id) as total_bookings from {Info.booking_table} as b
            inner join {Info.tour_option_table} as top on top.tour_option_id = b.tour_option_id
            group by b.tour_id limit 100
            """
        return query

    def list_of_promoted_tours(self) -> str:
        return """
            select p.tour_id from promoted_tour  as p
            inner join tour as t on t.tour_id = p.tour_id
            where creation_timestamp >= "2020-03-16" and t.assessment_status="in_progress" limit 300;
            """
