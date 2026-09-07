import os
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("ecommerce-daily-etl").enableHiveSupport().getOrCreate()
input_path = os.getenv("INPUT_PATH", "hdfs://namenode:9000/ecommerce/raw/*/*/*/*")

events = spark.read.json(input_path)
purchases = events.filter(F.col("event_type") == "purchase").withColumn(
    "revenue", F.col("price") * F.col("quantity")
)

# groupBy provoca shuffle e demonstra uma wide dependency.
daily_sales = purchases.groupBy("category", "region").agg(
    F.round(F.sum("revenue"), 2).alias("total_revenue"),
    F.sum("quantity").alias("items_sold"),
    F.countDistinct("event_id").alias("purchases"),
)

daily_sales.show(truncate=False)
spark.sql("CREATE DATABASE IF NOT EXISTS ecommerce")
daily_sales.write.mode("overwrite").saveAsTable("ecommerce.daily_sales")
spark.stop()
