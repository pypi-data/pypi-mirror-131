import json
import logging
from functools import reduce

from grimoire.gyg.data_analysis.domain.data_information import Info
from grimoire.json import print_pretty
from grimoire.time import Date


class BaseAnalysis:
    def __init__(self, spark):
        self.spark = spark

    def return_df(self, df, take_first=500):
        results = df.toJSON().take(take_first)

        if not results:
            return {"result": []}

        json_str = (
            '{"result": [' + reduce(lambda x, y: x + "," + str(y), results) + "]}"
        )

        print_pretty(json.loads(json_str))

    def sample_row(self, table_name):
        """
        Returns a row from the given table
        """

        return print_pretty(self.spark().table(table_name).limit(1).toJSON().first())

    def create_table_from_event(
        self,
        event_name,
        table_name,
        raw=False,
        single_day=None,
        only_yesterday=False,
        global_view=False,
    ):
        folder = Info.cleaned_events_folder
        if raw:
            folder = Info.raw_events_folder

        optional_date = ""
        if only_yesterday:
            optional_date = "/date=" + Date.yesterday_str()

        if single_day:
            optional_date = f"/date={single_day}"

        path = folder + "/" + event_name + optional_date
        logging.info(f"Event path to be created as table:  {path}")
        parquet = self.spark().read.parquet(path)

        if global_view:
            print("Creating global view")
            parquet.createOrReplaceGlobalTempView(table_name)
        else:
            parquet.createOrReplaceTempView(table_name)

        return parquet

    def sql(self, query):
        print(f"Final query: {query}")
        return self.spark().sql(query)

    def sample_event(self, event_name, date="yesterday"):
        """
        Create a table with the given event name and return 1 value out of this table
        """

        date = Date.parse_str(date)

        df = self.sql(
            f"""
            select *
                from events
                where
                    event_name = "{event_name}"
                    and date = "{date}" LIMIT 1
            """
        )

        return self.return_df(df)

    def metadata(self):

        yesterday = Date.yesterday_str()
        df = self.spark().sql(
            f"""
            select ui.metadata
                from events
                where
                    event_name = "UIClick"
                    and date = "{yesterday}" LIMIT 1
            """
        )

        import json

        final = df.rdd.map(json.loads).toDF()

        return self.return_df(final)
