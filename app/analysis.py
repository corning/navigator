import pandas as pd
import tushare as ts
import config
import os
import sys
import datetime
import decimal
from utils import Stock
from color_log import Logger

engine = config.get_db_engine()
stock = Stock()
log = Logger()

all_stocks=pd.read_sql_query('select * from stocks;', engine)

date='2020-02-28'
result_path = config.get_result_path(date+'.txt')
result=open(result_path,'r').read()
result_array=result.split(',')
# 持有天数
resutl_days=3
result_gt_10percent=[]
result_bt_5to10_percent=[]
result_bt_0to5_percent=[]
result_lt_0_percent=[]
for i in range(len(result_array)):
    stock=result_array[i]
    stock_row=all_stocks.loc[all_stocks['code']==stock,['table_name']]
    table=stock_row.loc[stock_row.index[0],'table_name']
    sql='select * from `'+table+'` where `date` >= "'+date+'"'
    col_res=pd.read_sql_query(sql,engine)
    dd=ts.get_sina_dd('002087',date='2020-02-28',vol=1000)
    # get_vol_building()
    print(dd)
    print(len(dd.loc[dd['type']=='买盘']))
    break
    buy_price = decimal.Decimal(col_res.loc[0,'close'])
    five_day_price = decimal.Decimal(col_res.loc[resutl_days,'close'])
    five_day_percent = round((five_day_price-buy_price)/buy_price*100,2)
    stock={stock:str(five_day_percent)+'%'}
    if five_day_percent>10:
        result_gt_10percent.append(stock)
    elif (five_day_percent>=5 and five_day_percent<=10):
        result_bt_5to10_percent.append(stock)
    elif (five_day_percent>=0 and five_day_percent <5):
        result_bt_0to5_percent.append(stock)
    else:
        result_lt_0_percent.append(stock)
# 五天后涨幅
str_days='持有'+str(resutl_days)+'天涨幅'
print(str_days+'>10% :'+str(len(result_gt_10percent))+'/'+str(len(result_array)))
print(result_gt_10percent)
print(str_days+' 5~10% :'+str(len(result_bt_5to10_percent))+'/'+str(len(result_array)))
print(result_bt_5to10_percent)
print(str_days+' 0~5% :'+str(len(result_bt_0to5_percent))+'/'+str(len(result_array)))
# print(result_bt_0to5_percent)
print(str_days+'< 0% :'+str(len(result_lt_0_percent))+'/'+str(len(result_array)))
# print(result_lt_0_percent)
