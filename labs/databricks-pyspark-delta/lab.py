"""Local Spark/Delta ingest, transform, merge, and partition inspection lab."""

import shutil
from pathlib import Path

from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
TABLE_PATH = OUTPUT / "orders_delta"

ORDER_SCHEMA = T.StructType(
    [
        T.StructField("order_id", T.IntegerType(), False),
        T.StructField("customer_id", T.StringType(), False),
        T.StructField("order_date", T.DateType(), False),
        T.StructField("quantity", T.IntegerType(), False),
        T.StructField("unit_price", T.DecimalType(10, 2), False),
        T.StructField("status", T.StringType(), False),
    ]
)


def build_spark() -> SparkSession:
    builder = (
        SparkSession.builder.appName("delta-merge-lab")
        .master("local[2]")
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.shuffle.partitions", "2")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


def read_orders(spark: SparkSession, filename: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("dateFormat", "yyyy-MM-dd")
        .schema(ORDER_SCHEMA)
        .csv(str(ROOT / "data" / filename))
    )


def validate(df: DataFrame, label: str) -> None:
    required = [field.name for field in ORDER_SCHEMA.fields]
    invalid = df.filter(
        F.greatest(*[F.col(column).isNull().cast("int") for column in required]) == 1
    ).count()
    invalid += df.filter((F.col("quantity") <= 0) | (F.col("unit_price") < 0)).count()
    duplicates = df.groupBy("order_id").count().filter(F.col("count") > 1).count()
    if invalid or duplicates:
        raise ValueError(
            f"{label}: invalid rows={invalid}, duplicate order IDs={duplicates}"
        )


def transform(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "order_total",
        F.round(F.col("quantity") * F.col("unit_price"), 2).cast(T.DecimalType(12, 2)),
    )


def show_partitions() -> None:
    print("\nPhysical partition directories:")
    partitions = sorted(
        path.relative_to(TABLE_PATH)
        for path in TABLE_PATH.glob("order_date=*")
        if path.is_dir()
    )
    for partition in partitions:
        parquet_count = len(list((TABLE_PATH / partition).glob("*.parquet")))
        print(f"  {partition} ({parquet_count} Parquet file(s))")


def main() -> None:
    shutil.rmtree(OUTPUT, ignore_errors=True)
    spark = build_spark()
    spark.sparkContext.setLogLevel("WARN")
    try:
        initial = read_orders(spark, "orders.csv")
        validate(initial, "initial ingest")
        (
            transform(initial)
            .write.format("delta")
            .mode("overwrite")
            .partitionBy("order_date")
            .save(str(TABLE_PATH))
        )

        updates = read_orders(spark, "order_updates.csv")
        validate(updates, "merge source")
        (
            DeltaTable.forPath(spark, str(TABLE_PATH))
            .alias("target")
            .merge(
                transform(updates).alias("source"),
                "target.order_id = source.order_id",
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )

        result = spark.read.format("delta").load(str(TABLE_PATH))
        print("\nMerged orders:")
        result.orderBy("order_id").show(truncate=False)
        print("Logical rows by partition key:")
        result.groupBy("order_date").count().orderBy("order_date").show()
        show_partitions()
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
