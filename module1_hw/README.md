Module 1 - Homework - Docker and terraform fundamentals
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/01-docker-terraform/homework.md

Question 1: Run Docker with Python 3.13 image using bash entrypoint.
(pipeline) > docker run -it -- entrypoint=bash python:3.13-slim
Unable to find image 'python:3.13-slim' locally
3.13-slim: Pulling from library/python

root@a457d09a8842:/# pip -- version
pip 26.0.1 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

Question 2: postgres: 5432

Question 3: For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?
SELECT COUNT(*) AS total_trips
FROM green_taxi_data
WHERE (lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1);
Answer: 6139 total trips

Question 4: Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).
QYERY: select trip_distance, lpep_pickup_datetime from 
green_taxi_data t
where trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
Answer: 2025-11-14

Question 5: Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?
Query: select z."Zone", SUM(total_amount) as total_amount
from green_taxi_data t
JOIN zones_lookup z
ON z."LocationID"=t."PULocationID"
where lpep_pickup_datetime >= '2025-11-18'
AND lpep_pickup_datetime < '2025-11-19'
group by z."Zone"
ORDER BY total_amount DESC
LIMIT 1;
Answer: East Harlem North - 9281.919 (total_amount)

Question 6: For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?
Query: select tip_amount, dz."Zone",t."DOLocationID",t."PULocationID"
from green_taxi_data t
JOIN zones_lookup pu
  ON pu."LocationID" = t."PULocationID"
JOIN zones_lookup dz
  ON dz."LocationID" = t."DOLocationID"
where pu."Zone" = 'East Harlem North'
AND lpep_pickup_datetime >= '2025-11-01'
and lpep_pickup_datetime < '2025-12-01'
ORDER BY tip_amount DESC
LIMIT 5
Answer: Yorkville West

Question 7: Question 7. 
Which of the following sequences, respectively, describes the terraform workflow for:

Downloading the provider plugins and setting up backend,
Generating proposed changes and auto-executing the plan
Remove all resources managed by terraform`
Answer: terraform init, terraform apply -auto-approve, terraform destroy
