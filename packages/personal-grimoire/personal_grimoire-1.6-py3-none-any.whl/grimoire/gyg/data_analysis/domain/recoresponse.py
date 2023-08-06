from grimoire.gyg.data_analysis.utils import BaseAnalysis
from grimoire.time.time import Date


class RecoResponse(BaseAnalysis):
    def create_tmp_table(
        self,
    ):

        date_from = "2019-09-01"
        date_to = "2019-12-19"
        date_from = "2019-12-19"
        table_name = "RecoResponseJean"

        self.create_table_from_event(
            "RecoResponse", table_name, single_day=date_from, raw=True, global_view=True
        )

    def requests_trend(
        self,
    ):

        date_from = "2019-09-01"
        date_to = "2019-12-19"
        table_name = "RecoResponseJean"

        df = self.create_table_from_event("RecoResponse", table_name, raw=True)
        df.cache()

        date_column = "event_properties.timestamp"

        df = self.sql(
            f"""
                select
                        count(1) as total,
                        FIRST(DATE({date_column})) as day
                    from {table_name}
                    where
                        DATE({date_column})<="{date_to}"
                        and DATE({date_column})>="{date_from}"
                    group by DAY({date_column})
                    order by day asc
            """
        )

        return self.return_df(df)

    def join(self):
        rr = self.cmd.create_table("RecoResponse", raw=True)
        ri = self.cmd.create_table("RecommendationsImpression", raw=True)
        joined = rr.join(ri, rr.service_uuid == ri.service_response_uuid)
        return joined.toJSON().first()

    def percentage_of_people_who_see_recos_in_adp(self):
        from pyspark.sql.functions import lit

        """
        how many users that sees recommendations when they access adp

        1 third as last queried
        {
          "count(1)": {
            "0": 130178,
            "1": 303468
          },
          "name": {
            "0": "RecommendationsImpression",
            "1": "ActivityDetailPageRequest"
          }
        }
        """
        self.cmd.create_table("ActivityDetailPageRequest")
        self.cmd.create_table("RecommendationsImpression")
        total_ri = self.spark.sql(
            f"select count(1) from RecommendationsImpression"
        ).withColumn("name", lit("RecommendationsImpression"))
        total_adpr = self.spark.sql(
            f"select count(1) from ActivityDetailPageRequest"
        ).withColumn("name", lit("ActivityDetailPageRequest"))
        # return stack_dfs(total_ri, total_adpr).toPandas().to_json()

    def targets(self):
        arr = self.cmd.create_table("ActivityRecommendationRequest", raw=True)
        return arr.select("target", "container_name").distinct().toPandas().to_json()

    def percentage_of_each_event(self):
        from pyspark.sql.functions import lit

        date = Date.yesterday_str()
        self.cmd.create_table("ActivityRecommendationRequest", raw=True)
        self.cmd.create_table("RecoResponse", raw=True)
        self.cmd.create_table("RecommendationsImpression", raw=True)

        total_rr = self.spark.sql(f"select count(1) from RecoResponse").withColumn(
            "name", lit("RecoResponse")
        )
        total_ri = self.spark.sql(
            f"select count(1) from RecommendationsImpression"
        ).withColumn("name", lit("RecommendationsImpression"))
        total_arr = self.spark.sql(
            f"select count(1) from ActivityRecommendationRequest"
        ).withColumn("name", lit("ActivityRecommendationRequest"))

        # return stack_dfs(total_rr, total_ri, total_arr).toPandas().to_json()
