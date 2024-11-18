from cleaner import *
from uploader import *
import pandas as pd

def caller_function_database():
    #reading csv and saving in database for better query
    df = pd.read_csv("./data.csv")
    create_schema_and_table(df)
