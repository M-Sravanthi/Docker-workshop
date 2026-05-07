#!/usr/bin/env python
# coding: utf-8

#get_ipython().system('uv add tqdm')
#get_ipython().system('uv add sqlalchemy')
#get_ipython().system('uv add psycopg2-binary')

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm



# Here,  we need to clean the table - make the columns into proper data types. For eg: VendorID should int and not float and pickupdatetime should by dateTime format. 

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# Now we will focus on exporting this data to postgres
# What you run here is similar to running it in terminal. So now we have to install a toolkit to use SQL commands within the python application - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
#print(pd.io.sql.get_schema(df,name='yellow_taxi_data',con=engine))
# This dataset is too big. So now we will only read chunks of this dataset at once and then insert the chunks into the table.


def run():
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'


    year = 2021
    month =1

    target_table = 'yello_taxi_data'
    chunksize = 100000

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    #posgresql://user:pass@localhost:port_No/db_name
    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")


    df_iter = pd.read_csv(url,
                     dtype=dtype,
                     parse_dates=parse_dates,
                     iterator = True,
                     chunksize = chunksize)
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace')
            first = False
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append')

if __name__ == '__main__':
    run()
















