import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime
from io import StringIO
import telegram

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.models import Variable

from urllib.parse import urlencode
import requests
import json

def ydisk(public_key, sep=None):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    if sep: 
        df = pd.read_csv(download_url, sep=';')
    else:
        df = pd.read_csv(download_url)
    return df

public_key = 'https://disk.yandex.com.am/d/dz4Vx8oLxd3nPA'

login = 'd-kalinin-42'
year = 1994 + hash(f'{login}') % 23

default_args = {
    'owner': 'd-kalinin-42',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 10, 29),
}


@dag(default_args=default_args, schedule_interval='0 12 * * *', catchup=False)
def games_kalinin_d():
    
    @task(retries=3)
    def get_data():     
        df = ydisk(public_key)
        df = df.query('Year == @year')
        return df

    @task()
    def get_top_1_games(df):
        top_1_games = df.groupby('Name', as_index=False).agg({'Global_Sales':'sum'}).sort_values('Global_Sales', ascending=False).head(1).Name.reset_index(drop= True)
        return top_1_games

    @task()
    def get_top_EU(df):
        max_EU_Sales = df.groupby('Genre',as_index=False).agg({'EU_Sales':'sum'}).sort_values('EU_Sales', ascending=False).head(1).iloc[0]['EU_Sales']
        df_top_EU = df.groupby('Genre', as_index=False).agg({'EU_Sales':'sum'}).query(f'EU_Sales == {max_EU_Sales}').Genre.reset_index(drop= True)
        return df_top_EU

    @task()
    def get_top_games_NA(df):
        max_NA_Sales_Platform_sum = df.groupby('Platform', as_index=False).agg({'NA_Sales':'sum'}).sort_values('NA_Sales', ascending=False).head(1).iloc[0]['NA_Sales']
        max_NA_Sales_Platform = df.groupby('Platform', as_index=False).agg({'NA_Sales':'sum'}).query(f'NA_Sales == {max_NA_Sales_Platform_sum}').Platform
        return max_NA_Sales_Platform

    @task()
    def get_top_Publisher_JP(df):
        max_mean_Publisher_JP = df.groupby('Publisher',as_index=False).agg({'JP_Sales':'mean'}).sort_values('JP_Sales', ascending=False).iloc[0]['JP_Sales']
        max_mean_sales_Publisher_JP = df.groupby('Publisher',as_index=False).agg({'JP_Sales':'mean'}).query(f'JP_Sales == {max_mean_Publisher_JP}').Publisher
        return max_mean_sales_Publisher_JP

    @task()
    def get_top_EU_or_JP(df):
        games_EU_sales = df.groupby('Name', as_index=False).agg({'EU_Sales':'sum'}).sort_values('EU_Sales', ascending=False)
        games_JP_sales = df.groupby('Name', as_index=False).agg({'JP_Sales':'sum'}).sort_values('JP_Sales', ascending=False)
        df_EU_and_JP = games_EU_sales.merge(games_JP_sales, on = 'Name')
        df_EU_and_JP['EU_difference_JP'] = df_EU_and_JP.EU_Sales - df_EU_and_JP.JP_Sales
        df_count_best_EU = df_EU_and_JP.query('EU_difference_JP>0').EU_difference_JP.count()
        return df_count_best_EU
    
    
    @task()
    def print_data(top_1_games, df_top_EU, max_NA_Sales_Platform, max_mean_sales_Publisher_JP, df_count_best_EU):

        print(f'Top 1 games in the reporting year {year} ')
        print(top_1_games)
        
        print(f'Games of the genre were the best-selling in Europe {year} ')
        print(df_top_EU)
        
        print(f'Top platform in north america {year} ')
        print(max_NA_Sales_Platform)
        
        print(f'Top publisher by average sales in Japan {year} ')
        print(max_mean_sales_Publisher_JP)
        
        print(f'Better game sales in europe compared to japan {year} ')
        print(df_count_best_EU)

    df = get_data()

    top_1_games = get_top_1_games(df)
    df_top_EU = get_top_EU(df)   
    max_NA_Sales_Platform = get_top_games_NA(df)
    max_mean_sales_Publisher_JP = get_top_Publisher_JP(df)
    df_count_best_EU = get_top_EU_or_JP(df)

    print_data(top_1_games, df_top_EU, max_NA_Sales_Platform, max_mean_sales_Publisher_JP, df_count_best_EU)

games_kalinin_d = games_kalinin_d()