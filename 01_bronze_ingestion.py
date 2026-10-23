# Databricks notebook source
# RetailPulse — Bronze ingestion
# Edit INPUT_PATH to the actual Unity Catalog Volume path for your Olist CSV.
from pyspark.sql import functions as F

INPUT_PATH = "/Volumes/<catalog>/<schema>/<volume>/olist_orders_dataset.csv"
CATALOG = "workspace"
SCHEMA = "retailpulse"
BRONZE_TABLE = f"{CATALOG}.{SCHEMA}.bronze_orders"

# Create schema once. In Unity Catalog, write to a fully qualified table name.
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

raw = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(INPUT_PATH)
)

# Keep source lineage using _metadata.file_path (input_file_name() may be unavailable
# in some Unity Catalog serverless contexts).
bronze = (
    raw
    .withColumn("_source_file", F.col("_metadata.file_path"))
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_ingestion_date", F.current_date())
)

(bronze.write
    .format("delta")
    .mode("overwrite")   # Use append only after you implement safe incremental ingestion.
    .option("overwriteSchema", "true")
    .saveAsTable(BRONZE_TABLE)
)

print(f"Bronze row count: {spark.table(BRONZE_TABLE).count()}")
display(spark.table(BRONZE_TABLE).limit(10))
