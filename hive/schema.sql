CREATE DATABASE IF NOT EXISTS ecommerce;

CREATE EXTERNAL TABLE IF NOT EXISTS ecommerce.raw_events (
  event_id STRING,
  event_type STRING,
  user_id STRING,
  product_id STRING,
  category STRING,
  price DOUBLE,
  quantity INT,
  region STRING,
  delivery_status STRING,
  event_time STRING
)
STORED AS TEXTFILE
LOCATION '/ecommerce/raw';
