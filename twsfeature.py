# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 07:48:16 2021

@author: Alvin
"""

import urllib3
from bs4 import BeautifulSoup

#資料處理套件
import pandas as pd
from datetime import date

#畫圖套件
import matplotlib.pyplot as plt

#from plotly.subplots import make_subplots
#import plotly.graph_objects as go

#下載多日台指期資料
def get_tw_futures(start_year, start_month, start_day, end_year, end_month, end_day, market_code = 0):
    start_date = str(date(start_year, start_month, start_day))
    end_date = str(date(end_year, end_month, end_day))
    date_list = pd.date_range(start_date, end_date, freq='D').strftime("%Y/%m/%d").tolist()

    df = pd.DataFrame()
    http = urllib3.PoolManager()
    url = "https://www.taifex.com.tw/cht/3/futDailyMarketReport"
    for day in date_list:  
        res = http.request(
             'POST',
              url,
              fields={
                 'queryType': 2,
                 'marketCode': market_code,
                 'commodity_id': 'TX',
                 'queryDate': day,
                 'MarketCode': market_code,
                 'commodity_idt': 'TX'
              }
         )
        html_doc = res.data
        soup = BeautifulSoup(html_doc, 'html.parser')
        table = soup.findAll('table')[2]
        df_day = pd.read_html(str(table))[2]
        #加入日期
        df_day.insert(0, '日期', day)
        df = df.append(df_day, ignore_index = True)
    
    return df

df = get_tw_futures(start_year = 2021, 
                    start_month = 10, 
                    start_day = 13, 
                    end_year = 2021, 
                    end_month = 10, 
                    end_day = 15)
#畫出台指期的走勢圖與K線圖
df_tx = df.loc[(df['到期月份(週別)'] == 202110.0)]


#畫出台指期走勢圖
fig = plt.figure(figsize = (10, 5))
plt.title('TX Price')
plt.plot(df_tx['日期'], df_tx['最後成交價'])
plt.plot(df_tx['日期'], df_tx['開盤價'])
plt.legend(['Close', 'Open'])



# 設x軸標題
fig.update_xaxes(title_text = "日期", 
                 rangebreaks = [{ 'pattern': 'day of week', 'bounds': [6, 1]}])

# 設y軸標題
fig.update_yaxes(title_text = "指數")

# 設圖標及圖長寬
fig.update_layout(
    title_text = "台指期K線圖 - 到期月份2021/10 ",
    width = 800,
    height = 400
)

fig.show()