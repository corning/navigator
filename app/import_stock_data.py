import pandas as pd
import sys
import os
import config
from utils import Stock

engine = config.get_db_engine()
stock = Stock()

# 把沪深两的二进制文件转换成csv文件
def insert_data_to_database(isStocks=False):
    folders = ['sh','sz']
    for folder in folders:
        shsz = folder
        path = 'vipdoc/'+ shsz +'/lday/'
        listfile = os.listdir(path)
        for i in listfile:
            print(i)
            if isStocks:
                df_write = pd.DataFrame({'code': str(i[2:8]), 'area': str(i[0:2]), 'table_name': str(i[0:8])}, index=["0"])
                print(df_write)
                df_write.to_sql('stocks', engine, index=False, if_exists='append')
            else :
                df = stock.read_tdx_lday_file(path+i)
                code = i.replace('.day','')
                df.to_sql(code, engine, index=True, if_exists='replace')
            
insert_data_to_database()