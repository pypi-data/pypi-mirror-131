#!/usr/bin/env python


from grimoire import s
from grimoire.gyg.data_analysis.domain.booking import Bookings
from grimoire.gyg.data_analysis.domain.recoresponse import RecoResponse
from grimoire.gyg.data_analysis.domain.visitor import Visitors
from grimoire.gyg.data_analysis.get_spark import GetSpark
from grimoire.gyg.data_analysis.utils import BaseAnalysis
from grimoire.time.time import Date


class Databricks(BaseAnalysis):
    """
    Databricks on local machine
    pre requirements to get dbconnect working:

    conda activate dbconnect
    do NOT have a spark home, you can do: unset SPARK HOME
    export DEBUG_IGNORE_VERSION_MISMATCH=1
    """

    def __init__(self):
        # self.cmd = DatabricksCmd(self.spark)
        # self.recoevents = RecoResponse(self.spark, self.cmd)
        self.spark = GetSpark().get
        self.visitor = Visitors
        self.booking = Bookings
        self.reco_response = RecoResponse

    def ls(self, path):
        return s.run(f"databricks fs ls dbfs:{path}")

    def list_tables(self):
        return self.spark().catalog.listTables()

    def info(self, table_name):
        """ Returns information about a given table"""

        self.schema(table_name)

        return self.spark().sql(f"Select count(1) from {table_name}")

    def schema(self, table_name):
        """returns the schema of a table"""
        return self.spark().table(table_name).printSchema()

    def events_names(self):
        """return the event names that were triggered yesterday"""

        yesterday = Date.yesterday_str()
        df = self.spark().sql(
            f"""
            select distinct(event_name) from events where date = "{yesterday}" LIMIT 500
            """
        )

        return self.return_df(df)

    def daily_count(self, event_name, days=30):

        df = self.cmd.create_table(event_name)
        import pyspark.sql.functions as F

        result = (
            df.select(F.date_format("date", "yyyy-MM-dd").alias("day"))
            .groupby("day")
            .count()
            .orderBy("day", ascending=False)
        )

        return self.return_df(result, days)


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(Databricks).start()
