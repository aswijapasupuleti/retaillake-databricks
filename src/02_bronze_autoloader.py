from pyspark.sql import functions as F

base = "/Volumes/retail/bronze/raw_landing"

def ingest(entity):
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.schemaLocation", f"{base}/_schemas/{entity}")
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .load(f"{base}/landing/{entity}")
        .withColumn("_ingest_time", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
        .writeStream
        .option("checkpointLocation", f"{base}/_checkpoints/{entity}")
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(f"retail.bronze.{entity}")
    )

for e in ["orders", "order_items", "order_payments", "customers", "products"]:
    ingest(e).awaitTermination()