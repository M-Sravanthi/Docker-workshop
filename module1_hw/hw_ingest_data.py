import pandas as pd
import click
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "ehail_fee": "float64",
    "trip_type": "float64",
    "cbd_congestion_fee": "float64"
}

parse_dates = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

@click.command()
@click.option('--pg_user', default='root', help='Postgres user')
@click.option('--pg_pass', default='root', help='Postgres password')
@click.option('--pg_host', default='pgdatabase', help='Postgres host')
@click.option('--pg_port', default=5432, type=int, help='Postgres port')
@click.option('--pg_db', default='ny_taxi', help='Postgres database name')
@click.option('--year', default=2025, type=int, help='Year of data')
@click.option('--month', default=11, type=int, help='Month of data')
@click.option('--target_table', default='green_taxi_data1', help='Target table name')
@click.option('--chunksize', default=5000, type=int, help='CSV read chunksize')

def run(pg_user, pg_pass, pg_port, pg_host, pg_db, target_table, month, year, chunksize):
    """Ingest green taxi data for a given year/month into Postgres."""

    prefix = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    url = f"{prefix}/green_tripdata_{year}-{month:02d}.parquet"
    df_parquet = pd.read_parquet(url)

    csv_file = f"green_tripdata_{year}-{month:02d}.csv"
    df_parquet.to_csv(csv_file, index=False)

    # postgresql://user:pass@localhost:port/db_name
    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")

    df_iter = pd.read_csv(
        csv_file,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists="replace")
            first = False

        df_chunk.to_sql(name=target_table, con=engine, if_exists="append")
    #Ingesting zones lookup csv file
    zone_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

    zones_df = pd.read_csv(zone_url)
    zones_df.to_sql(con=engine, 
                    name='zones_lookup1', 
                    if_exists='replace')



if __name__ == '__main__':
    run()

