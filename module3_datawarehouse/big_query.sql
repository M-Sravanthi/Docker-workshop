-- Query public available table
SELECT
    station_id,
    name
FROM bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;

-- Create an external table referencing files in GCS
CREATE OR REPLACE EXTERNAL TABLE `projectID.datasetID.external_yellow_tripdata`
OPTIONS (
    format = 'CSV',
    uris = [
        'gs://GCS_bucketName/yellow_tripdata_2019-*.csv', 
    ]
);

-- Preview yellow trip data from the external table
SELECT *
FROM projectID.datasetID.external_yellow_tripdata
LIMIT 10;

-- Create a non-partitioned table from the external table
CREATE OR REPLACE TABLE projectID.datasetID.yellow_tripdata_non_partitioned AS
SELECT *
FROM projectID.datasetID.external_yellow_tripdata;

-- Create a partitioned table from the external table
CREATE OR REPLACE TABLE projectID.datasetID.yellow_tripdata_partitioned
PARTITION BY DATE(tpep_pickup_datetime) AS
SELECT *
FROM projectID.datasetID.external_yellow_tripdata;

-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM projectID.datasetID.yellow_tripdata_non_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM tprojectID.datasetID.ellow_tripdata_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Inspect table partitions
SELECT
    table_name,
    partition_id,
    total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitioned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE projectID.datasetID.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * 
FROM projectID.datasetID.external_yellow_tripdata;

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM projectID.datasetID.yellow_tripdata_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM projectID.datasetID.yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
