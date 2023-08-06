import logging
import os


class GetSpark:
    _spark = None

    def get(self):
        if self._spark:
            return self._spark

        print("Initializing spark via dbconnect")

        logging.info("Initializing spark via dbconnect")

        if os.getenv("CONDA_DEFAULT_ENV") != "dbconnect":
            raise Exception("Db connect conda envioroment not active.")

        def unset_env(env):
            try:
                os.unsetenv(env)
                del os.environ[env]
            except:
                pass

        unset_env("SPARK_HOME")
        unset_env("PYSPARK_SUBMIT_ARGS")
        unset_env("PYTHONPATH")
        unset_env("PYSPARK_DRIVER_PYTHON")
        unset_env("PYSPARK_DRIVER_PYTHON_OPTS")
        import findspark

        findspark.init(
            spark_home="/home/jean/anaconda3/envs/dbconnect/lib/python3.7/site-packages/pyspark"
        )

        from pyspark.sql import SparkSession

        self._spark = SparkSession.builder.config(
            "spark.driver.memory", "10g"
        ).getOrCreate()

        return self._spark
