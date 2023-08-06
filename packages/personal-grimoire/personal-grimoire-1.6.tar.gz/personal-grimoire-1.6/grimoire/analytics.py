# type: ignore
# aliases
sql = lambda sql: spark.sql(sql)
s = sql
d = lambda x: display(x)


def sample(dataframe):
    """
    sample a dataframe
    """
    return dataframe.sample(False, 0.1, 0.1)


def group_by_date(df, timestamp_format, column_name="date"):
    """
    group dataframe by a date column with a format %d will filter by date, %d-%m by date and month

    use like:
    display(ga.group_by_date(a, '%w').count())
    """
    import pyspark.sql.functions as f

    return df.select(
        f.date_format(column_name, timestamp_format).alias("groupby_date_col")
    ).groupBy("groupby_date_col")


def stack_dfs(*dfs):
    """
    gets a list of data frames with the same schema and append one after the other
    as if they were get_options_cmd of the same table
    """
    from functools import reduce

    from pyspark.sql import DataFrame

    return reduce(DataFrame.unionAll, dfs)
