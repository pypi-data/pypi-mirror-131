class AnalysisPeriod:
    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

    def sql(self, column_name):
        return f' {column_name}>"{self.date_from}" and {column_name}<"{self.date_to}"'
