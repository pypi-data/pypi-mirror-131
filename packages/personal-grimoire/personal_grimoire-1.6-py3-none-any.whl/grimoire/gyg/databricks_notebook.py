class DatabricksNotebook:
    def __init__(self, globals):
        self.globals = globals
        self.spark = globals["spark"]

    def sql(self, sql: str, display=False, summary=False):
        print(f"Sql: {sql}")

        result = self.globals["spark"].sql(sql)
        if display:
            self.globals["display"](result)

        if summary:
            self.summary(result)

        return result

    def summary(self, df):
        print(f"Count: {df.count()}")

    def one_from_table(self, table_name, display=True):
        result = self.spark.table(table_name).limit(1)

        if display:
            self.globals["display"](result)

        return result
