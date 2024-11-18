import psycopg2
from psycopg2 import sql

connection = psycopg2.connect(
    host="localhost",
    database="dbname",
    user="postgres",
    password="1234"
)
#check weather the given chema and table is already there to save memory
def check_schema_and_table_exist(connection = connection, schema_name = "zomato_schema", table_name = "zomato_data"):
    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Define the query to check if schema exists
        schema_query = sql.SQL("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name = %s
        """)

        # Execute the query for the schema
        cursor.execute(schema_query, (schema_name,))
        schema_exists = cursor.fetchone() is not None

        if not schema_exists:
            return 0

        # Define the query to check if table exists within the schema
        table_query = sql.SQL("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
        """)

        # Execute the query for the table
        cursor.execute(table_query, (schema_name, table_name))
        table_exists = cursor.fetchone() is not None

        # Close the cursor
        cursor.close()

        return 1 if table_exists else 0

    except Exception as e:
        print(f"Error checking schema and table existence: {e}")
        return 0

