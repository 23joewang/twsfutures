# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 07:48:16 2021

@author: Alvin
"""

import twstock
import datetime
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

#print(twstock.codes)
#print(twstock.codes['6207'])

# 這是抓取歷史資料
stock_6207 = twstock.Stock('6207')

price_6207 = stock_6207.price[-5:]       # 近五日之收盤價
high_6207 = stock_6207.high[-5:]         # 近五日之盤中高點
low_6207 = stock_6207.low[-5:]           # 近五日之盤中低點
date_6207 = stock_6207.date[-5:]         # 近五日的日期

print('price_6207--->', price_6207)
print('high_6207--->', high_6207)
print('low_6207--->', low_6207)
print('date_6207--->', date_6207)

stock_6207_2017_10 = stock_6207.fetch(2017,10)      # 獲取 2017 年 10 月之股票資料


stock_6207_2018 = stock_6207.fetch_from(2018,1)     # 獲取 2018 年 01 月至今日之股票資料
stock_6207_2018_pd = pd.DataFrame(stock_6207_2018)
stock_6207_2018_pd = stock_6207_2018_pd.set_index('date')

chinese_font = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\kaiu.ttf")

fig = plt.figure(figsize=(10, 6))
plt.plot(stock_6207_2018_pd.close, '-' , label="收盤價")
plt.plot(stock_6207_2018_pd.open, '-' , label="開盤價")
plt.title('雷科股份2018 開盤/收盤價曲線',loc='right',fontproperties=chinese_font)
# loc->title的位置
plt.xlabel('日期',fontproperties=chinese_font)
plt.ylabel('收盤價',fontproperties=chinese_font)
plt.grid(True, axis='y')
plt.legend(prop=chinese_font)
plt.show()
fig.savefig('day20_01.png')

from twstock import Stock

stock = Stock('2330')                             # 擷取台積電股價
ma_p = stock.moving_average(stock.price, 5)       # 計算五日均價
ma_c = stock.moving_average(stock.capacity, 5)    # 計算五日均量
ma_p_cont = stock.continuous(ma_p)                # 計算五日均價持續天數
ma_br = stock.ma_bias_ratio(5, 10)                # 計算五日、十日乖離值


from twstock import BestFourPoint

stock = Stock('2330')
bfp = BestFourPoint(stock)

print(bfp.best_four_point_to_buy())    # 判斷是否為四大買點
print(bfp.best_four_point_to_sell())   # 判斷是否為四大賣點
print(bfp.best_four_point())       # 綜合判斷