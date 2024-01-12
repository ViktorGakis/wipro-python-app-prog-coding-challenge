from pyspark.sql import DataFrame, SparkSession
from src import Config, DataSummary, LoadTxtData, Spark, TxtSchemaProvider

config = Config()


def main() -> None:
    config = Config()
    spark: SparkSession = Spark(config).create()
    df_txt: DataFrame = LoadTxtData(
        spark, TxtSchemaProvider.schema, config.TXT_FILE_REL_PATH_STR  # type: ignore
    ).load_source_file()
    DataSummary.display_summary(df_txt)


if __name__ == "__main__":
    main()
