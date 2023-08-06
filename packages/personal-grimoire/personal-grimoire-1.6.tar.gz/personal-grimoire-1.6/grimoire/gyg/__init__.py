# type: ignore
import logging

from grimoire.time import Date


class DatabricksCmd:
    def from_notebook_globals(self, context):
        """use like CmdfromN_notebook_globals(context)"""
        return DatabricksCmd(context["spark"], context)

    def __init__(self, spark, context={}):
        """Global object to be interacted """
        self.spark = spark
        self.context = context

    def ls(self, path):
        return self.context["dbutils"].fs.ls(path)

    def list_all_clean_events(self):
        return self.context["dbutils"].fs.ls("/mnt/analytics/cleaned/v1")

    def list_events(self):
        return self.ls(config["raw_events_folder"])

    def sql(self, query):
        return self.context["spark"].sql(query)

    def d(self, x):
        return self.context["display"](x)

    def create_table_from_event(self, event_name, raw=False, only_yesterday=False):
        folder = config["cleaned_events_folder"]
        if raw:
            folder = config["raw_events_folder"]

        optional_date = ""
        if only_yesterday:
            optional_date = "/date=" + Date.yesterday_str()

        path = folder + "/" + event_name + optional_date
        logging.info(f"Event path to be created as table:  {path}")
        parquet = self.spark.read.parquet(path)
        parquet.createOrReplaceTempView(event_name)
        return parquet

    def help(self) -> str:
        return f"""
        A wrapper for gyg commands
        Commands:

        {dir(DatabricksCmd)}

        """


def is_virtualproduct(self, tour):
    return tour.user_id == 0
