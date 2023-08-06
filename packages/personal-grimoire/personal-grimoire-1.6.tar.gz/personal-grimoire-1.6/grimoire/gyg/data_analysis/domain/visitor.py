from grimoire.gyg.data_analysis.domain.data_information import Info
from grimoire.gyg.data_analysis.get_spark import GetSpark
from grimoire.gyg.data_analysis.utils import BaseAnalysis
from grimoire.time import Date


class Visitors(BaseAnalysis):
    def __init__(self, spark):
        self.spark

    def adp_visits_for_visitor(self, visitor_id):
        """return the event names that were triggered yesterday"""

        yesterday = Date.yesterday_str()
        df = self.spark.sql(
            f"""
            select pageview_properties.tour_ids
                from events
                where event_name='ActivityDetailPageRequest'
                and date = "{yesterday}"
                and user.visitor_id = "{visitor_id}"
                LIMIT 500
            """
        )
        return self.return_df(df)

    def number_of_visitors(self):
        """return the event names that were triggered yesterday"""

        yesterday = Date.yesterday_str()
        df = self.spark().sql(
            f"""
            select count(distinct(user.visitor_id)) as total_visitors
                from events
                where event_name='ActivityDetailPageRequest'
                and date = "{yesterday}"
                LIMIT 500
            """
        )

        return self.return_df(df)

    def number_of_visitors_raw(self):
        date_to = Date.yesterday_str()
        path = f"{Info.raw_events_folder}/{Info.adp_event}/date={date_to}"

        parquet = self.spark().read.parquet(path)
        event_table = "raw_events"
        parquet.createOrReplaceTempView(event_table)

        df = self.spark().sql(
            f"""
              SELECT
                count(distinct(user.visitor_id)) as total_visitors
              FROM {event_table}
            """
        )

        return self.return_df(df)

    def ids(self):

        date = Date.yesterday_str()

        df = self.spark().sql(
            f"""
  SELECT
     user.visitor_id AS visitor_id
  FROM events
  WHERE
    date = "{date}"
    AND event_name = "ActivityDetailPageRequest" LIMIT 500
        """
        )

        return self.return_df(df)
