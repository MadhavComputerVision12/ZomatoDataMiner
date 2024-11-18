import json
import pandas as pd
import numpy as np
#clean the json files given 
def path_list_f():
    path1 = "./archive/file1.json"
    path2 = "./archive/file2.json"
    path3 = "./archive/file3.json"
    path4 = "./archive/file4.json"
    path5 = "./archive/file5.json"
    path_list = [path1,path2,path3,path4,path5]
    return path_list
#make basic df after cleaning
def df_maker(path_list):
    final_list = []
    for path in path_list:
        with open(path, 'r') as file:
            data = json.load(file)
            for ele in data:
                if 'message' not in ele.keys() :
                    final_list.append(ele['restaurants'])
    final_list2 = []
    for ele in final_list:
        for ele2 in ele:
            final_list2.append(ele2['restaurant'])
    temp = pd.DataFrame(final_list2)
    return temp


#expand json to columns
def expand_dict_columns(df, columns):
    for column in columns:
        if column in df.columns:
            expanded_df = df[column].apply(lambda x: pd.Series(x) if isinstance(x, dict) else pd.Series())
            df = pd.concat([df.drop(columns=[column]), expanded_df], axis=1)
    return df



def driver_cleaner():
    path_list = path_list_f()
    temp = df_maker(path_list)
    df_temp = expand_dict_columns(temp, columns = ['user_rating' , 'R' ,'location' ,'zomato_events'])
    temp = pd.read_excel('./archive/Country-Code.xlsx')
    temp.columns = ['country_id','Country']
    df_temp = df_temp.merge(temp, on='country_id', how='left')
    df_temp.to_csv("./data.csv")