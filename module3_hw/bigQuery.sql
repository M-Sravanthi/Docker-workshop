CREATE OR REPLACE EXTERNAL TABLE `projectID.datasetID.yellow_taxi_external_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://gcs_bucket/rides_dataset/rides/*.parquet']
);

SELECT   table_catalog,
  table_schema,
  table_name
FROM `projectID.datasetID.INFORMATION_SCHEMA.TABLES`;

SELECT count(*) FROM `projectID.datasetID.yellow_taxi_external_2024`;

CREATE OR REPLACE TABLE `projectID.datasetID.yellow_taxi_regular_2024`
AS
SELECT *
FROM `projectID.datasetID.yellow_taxi_external_2024`;


SELECT COUNT(DISTINCT pu_location_id) AS uniqueID
FROM `projectID.datasetID.yellow_taxi_external_2024`;

SELECT COUNT(DISTINCT pu_location_id) AS uniqueID
FROM `projectID.datasetID.yellow_taxi_regular_2024`;

SELECT pu_location_id FROM
 `kprojectID.datasetID.yellow_taxi_regular_2024`;

SELECT pu_location_id,do_location_id FROM
`projectID.datasetID.yellow_taxi_regular_2024`;

SELECT COUNT(fare_amount) AS zero_fare_trips FROM 
`projectID.datasetID.yellow_taxi_regular_2024`
WHERE fare_amount=0 ;

CREATE OR REPLACE TABLE `projectID.datasetID.yellow_taxi_2024partition`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY vendor_id
AS
SELECT *
FROM `projectID.datasetID.yellow_taxi_regular_2024`;

SELECT vendor_id from `projectID.datasetID.yellow_taxi_2024partition`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-16';

Select COUNT(*) from `projectID.datasetID.yellow_taxi_regular_2024`;






