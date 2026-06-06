

Create an external table: 
CREATE OR REPLACE EXTERNAL TABLE `project.dataset.yellow_taxi_external_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket/*.parquet']
);


Create a regular table:


Question 1. Counting records
What is count of records for the 2024 Yellow Taxi Data?
Ans: 20,332,093

Question 2. Data read estimation
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
THe bytes billed and processed are the same for both - only query estimation differed -- it showed 0Bytes will be processed for external table and 155MB for regular table. 
Ans: 0 MB for the External Table and 155.12 MB for the Materialized Table

Question 3. Understanding columnar storage
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.

Why are the estimated number of Bytes different?
155MB for scanning 1 column and 310MB for scanning two columns.

Question 4. Counting zero fare trips
How many records have a fare_amount of 0?
Ans: 8333

Question 5. Partitioning and clustering
Ans: Partition by tpep_dropoff_datetime and Cluster on VendorID

Question 6: Partition benefits
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?
Ans: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

Question 7: External table storage
Where is the data stored in the External Table you created?
Ans: GCP Bucket

Question 8. Clustering best practices
It is best practice in Big Query to always cluster your data: False

Question 9. Understanding table scans
rite a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
Ans: BigQuery can often answer COUNT(*) from table metadata/statistics without scanning the table data itself.

