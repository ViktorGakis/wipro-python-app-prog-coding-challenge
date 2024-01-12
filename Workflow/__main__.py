from pyspark.sql import DataFrame, SparkSession
from src import (
    CalculationEngine,
    Config,
    DataPreprocessor,
    DataSummary,
    LoadTxtData,
    Spark,
    TxtSchemaProvider,
)

config = Config()


def main() -> None:
    config = Config()
    spark: SparkSession = Spark(config).create()
    print("------------------------------")
    print("LOADING .TXT FILE")
    print("------------------------------")
    df_txt: DataFrame = LoadTxtData(
        spark, TxtSchemaProvider.schema, config.TXT_FILE_REL_PATH_STR  # type: ignore
    ).load_source_file()
    DataSummary.display_summary(df_txt)
    print("\n")
    print("------------------------------")
    print("DF_FILTERED")
    print("------------------------------")
    df_processed: DataFrame = DataPreprocessor.run(df_txt, config)
    DataSummary.display_summary(df_processed)
    print("------------------------------")
    print(" ")
    print("CalculationEngine")
    CalculationEngine.run(df_processed)


if __name__ == "__main__":
    main()
