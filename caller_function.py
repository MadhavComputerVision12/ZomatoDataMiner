from query import *
from caller_function_database import *
#caller function to simulate everything
def caller_function(locality_name,city_name,country,cuisine,filter,filter_param):
    df_final = filter_f(locality_name, city_name,country,cuisine, filter, filter_param)
    return df_final
