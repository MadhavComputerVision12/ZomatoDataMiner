import psycopg2
import sqlalchemy
from datetime import datetime
from cleaner import *

conn_params = {
    'dbname': 'dbname',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}
#function to upload the data to database
def create_schema_and_table(df):
    connx = psycopg2.connect(**conn_params)
    cur = connx.cursor()
    cur.execute(f'''create schema if not exists zomato_schema ;''')
    connx.commit()
    postgres_connection_string = f'postgresql://postgres:1234@localhost:5432/dbname'
    engine = sqlalchemy.create_engine(postgres_connection_string)
    print(df)
    #table_name = "zomato_data" schema = variable schema_name
    df.to_sql("zomato_data", engine, schema="zomato_schema", if_exists='append', index=False)
    cur.close()
    connx.close()
