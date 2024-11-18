import pandas as pd
import psycopg2

# Define connection parameters
conn_params = {
    'dbname': 'dbname',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5430'
}

# Create a function to establish a database connection
def get_connection(conn_params):
    conn = psycopg2.connect(**conn_params)
    return conn

# Query 1: Fetch records based on city and locality
def query1(conn, city_name, locality_name, country, cuisine):
    cursor = conn.cursor()
    query = '''
    SELECT * FROM zomato_schema.zomato_data
    WHERE "Country" = %s AND city = %s AND locality = %s;
    '''
    cursor.execute(query, (country, city_name, locality_name))
    records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names
    records_df = pd.DataFrame(records, columns=column_names)
    cursor.close()
    return records_df

# Query 2: Fetch records based on city, locality, and id
def query2(conn, city_name, locality_name, id, country, cuisine):
    cursor = conn.cursor()
    query = '''
    SELECT * FROM zomato_schema.zomato_data
    WHERE "Country" = %s AND city = %s AND locality = %s AND res_id = %s;
    '''
    cursor.execute(query, (country, city_name, locality_name, id))
    records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names
    records_df = pd.DataFrame(records, columns=column_names)
    cursor.close()
    return records_df

# Query 3: Fetch records based on city, locality, and name
def query3(conn, city_name, locality_name, name, country, cuisine):
    cursor = conn.cursor()
    query = '''
    SELECT * FROM zomato_schema.zomato_data
    WHERE "Country" = %s AND city = %s AND locality = %s AND name = %s;
    '''
    cursor.execute(query, (country, city_name, locality_name, name))
    records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names
    records_df = pd.DataFrame(records, columns=column_names)
    cursor.close()
    return records_df

# Function to map ratings to numeric values
def make_ratings(df):
    rating_map = {
        'Poor': 0,
        'Not rated': 2,
        'Average': 5,
        'Good': 7,
        'Very Good': 8,
        'Excellent': 10
    }
    # Apply the mapping to the DataFrame
    df['numeric_ratings'] = df['rating_text'].map(rating_map)
    return df

# Main function to apply filters and sort data
def filter_f(locality_name, city_name, country, cuisine, filter, filter_param):
    conn = get_connection(conn_params)
    df_final = pd.DataFrame()
    
    if filter == 1:
        df = query1(conn, city_name, locality_name, country, cuisine)
        df = make_ratings(df)
        df_final = df.sort_values(by='numeric_ratings', ascending=not bool(int(filter_param)))
    elif filter == 2:
        df = query1(conn, city_name, locality_name, country, cuisine)
        df = make_ratings(df)
        df['average_cost_for_two'] = df['average_cost_for_two'].astype(int)
        df_final = df.sort_values(by='average_cost_for_two', ascending= not bool(int(filter_param)))
    elif filter == 3:
        df_final = query3(conn, city_name, locality_name, filter_param, country, cuisine)
    elif filter == 4:
        df_final = query2(conn, city_name, locality_name, filter_param, country, cuisine)

    conn.close()
    
    if not df_final.empty:
        df_final = df_final.drop_duplicates(subset=['res_id'])
    
    return df_final

# Example usage
# df = filter_f('LocalityName', 'CityName', 'Country', 'Cuisine', 1, '0')
# print(df)
