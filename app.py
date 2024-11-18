from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import pandas as pd
from caller_function import *
from check import *

app = Flask(__name__)
app.secret_key = b'Royalh'

driver_cleaner()
print("Executed")
if not check_schema_and_table_exist():
    caller_function_database()

main_df = pd.read_csv("./data.csv")
# Convert DataFrame to dictionaries
cities_by_country = main_df.groupby('Country')['city'].unique().apply(list).to_dict()
localities_by_city = main_df.groupby('city')['locality'].unique().apply(list).to_dict()


df = None
@app.route('/')
def index():
    return render_template('input.html', cities_by_country=cities_by_country, localities_by_city=localities_by_city)

@app.route('/submit',methods=['POST'])
def submit():
    global df
    locality = request.form['locality']
    city = request.form['city']
    country = request.form['country']
    #cuisine = request.form['cuisine']
    cuisine = 'None'
    filter_option = request.form['filter']
    filter_param = request.form['filter_param']
    print("Filter =  ", filter_option)
    filter_option = int(filter_option)
    df = caller_function(locality,city,country,cuisine,filter_option,filter_param)
    #changing the column names and order for better visiblity
    df_show = df.drop(columns = ['Unnamed: 0','photos_url', 'url','apikey','deeplink','menu_url','book_url', 'switch_to_order_menu', 'featured_image', 'currency', 'id', 'establishment_types', 'events_url', 'order_deeplink','order_url','rating_color','latitude','country_id','locality_verbose', 'city_id', 'zipcode', 'longitude','is_delivering_now','has_table_booking','city','locality','Country','numeric_ratings','votes','rating_text','thumb'])
    df_show['has_online_delivery'] = df_show['has_online_delivery'].replace({1: 'Yes', 0: 'No'})
    #df_show['is_delivering_now'] = df_show['is_delivering_now'].replace({1: 'Yes', 0: 'No'})
    df_show['price_range'] = df_show['price_range'].replace({1: '$', 2: '$$', 3:'$$$',4:'$$$$'})
    df_show['offers'] = df_show['offers'].replace({'[]':'No'})
    #df_show['has_table_booking'] = df_show['has_table_booking'].replace({1: 'Yes', 0: 'No'})
    new_order = ['name', 'res_id', 'aggregate_rating','cuisines','price_range','has_online_delivery','offers']
    df_show = df_show[new_order]
    df_show.columns = ['Name','Restuarant ID','User Rating','Cuisines','Cost','Online Delivery','Offers']
    #df_show.reset_index(drop=True, inplace=True)
    #df_show.index = df_show.index + 1
    return render_template('index.html', tables=[df_show.to_html(classes='data', header="true")], titles=df_show.columns.values)

@app.route('/row/<int:index>')
def show_row(index):
    global df
    row = df.iloc[index]
    return render_template('row.html', row=row)




