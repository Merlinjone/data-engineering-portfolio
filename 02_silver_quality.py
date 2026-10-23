# Databricks notebook source
# RetailPulse — Silver cleansing and data quality
from pyspark.sql import functions as F
from pyspark.sql.window import Window

BRONZE_TABLE = "workspace.retailpulse.bronze_orders"
SILVER_TABLE = "workspace.retailpulse.orders_silver"
QUARANTINE_TABLE = "workspace.retailpulse.orders_quarantine"

bronze = spark.table(BRONZE_TABLE)

# Rename/normalize only when the source columns exist.
# Olist orders dataset commonly contains order_id, customer_id, order_status,
# order_purchase_timestamp, order_approved_at, order_delivered_carrier_date,
# order_delivered_customer_date, order_estimated_delivery_date.
required = ["order_id", "customer_id", "order_status"]
missing = [c for c in required if c not in bronze.columns]
if missing:
    raise ValueError(f"Required source columns missing: {missing}")

clean = bronze
for c in ["order_status"]:
    clean = clean.withColumn(c, F.lower(F.trim(F.col(c))))

# Parse known timestamp fields only when present.
timestamp_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
for c in timestamp_cols:
    if c in clean.columns:
        clean = clean.withColumn(c, F.to_timestamp(F.col(c)))

# Example data-quality rules: key must exist; duplicate order_id keeps newest ingestion.
invalid = clean.filter(
    F.col("order_id").isNull() |
    (F.trim(F.col("order_id")) == "") |
    F.col("customer_id").isNull()
)

valid = clean.join(
    invalid.select("order_id").where(F.col("order_id").isNotNull()).distinct(),
    on="order_id",
    how="left_anti"
)

w = Window.partitionBy("order_id").orderBy(F.col("_ingested_at").desc_nulls_last())
deduped = (
    valid.withColumn("_rn", F.row_number().over(w))
         .filter(F.col("_rn") == 1)
         .drop("_rn")
)

(invalid.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
 .saveAsTable(QUARANTINE_TABLE))
(deduped.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
 .saveAsTable(SILVER_TABLE))

print("Bronze:", bronze.count())
print("Quarantined:", invalid.count())
print("Silver:", spark.table(SILVER_TABLE).count())
print("Null order IDs in Silver:", spark.table(SILVER_TABLE).filter(F.col("order_id").isNull()).count())
display(spark.table(SILVER_TABLE).limit(10))
