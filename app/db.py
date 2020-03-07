import pandas as pd
import tushare as ts
import config
import datetime
from utils import Stock
from color_log import Logger

engine = config.get_db_engine()
stock = Stock()
log = Logger()

# 从数据库中读取数据并一条条读取今天实时数据并更新
def get_today_stock_data():
    sql_query = 'select * from stocks;'
    df_read = pd.read_sql_query(sql_query, engine)
    # 哪些已经更新过今天数据的计数器
    # DELETE FROM `sh600866` WHERE date='2020-03-03'
    count_array = []
    for index, row in df_read.iterrows():
        cur_real_df = ts.get_realtime_quotes(row['code'])
        today_date = cur_real_df.loc[0,'date']
        # cur_query = 'select * from `' + row['table_name'] +"` where date in ('" + today_date +"');"
        cur_df = pd.read_sql_query('select * from '+row['table_name'],engine)
        find_res = cur_df.loc[cur_df['date'] == today_date].head()
        if len(find_res) == 0:
            inser_row = stock.get_insert_row(cur_real_df)
            print('Insert today data ==> '+row['code'])
            print(inser_row)
            df_write = pd.DataFrame(inser_row, index=[len(cur_df)])
            df_write.to_sql(row['table_name'], engine, index=True, if_exists='append')
        else :
            count_array.append(row['code'])

    print(count_array)

# 一次性获取所有今天股票实时数据并更新数据库
def get_today_stock_data2():
    today_all=ts.get_today_all()
    df = pd.DataFrame(today_all)
    for index, row in df.iterrows():
        print(row)
        break

# 从数据库中读取数据并算出结果
def get_result_from_db():
    sql_query = 'select * from stocks;'
    # 使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
    df_read = pd.read_sql_query(sql_query, engine)
    filter_result = []
    filter_result_none=[]
    for index, row in df_read.iterrows():
        df = pd.read_sql_query('select * from '+row['table_name'], engine)
        diff=stock.get_MACD(df,12,26,9)
        if diff != 1 :
            filter_result.append(row['code'])
            log.info(row['table_name'])
        else :
            filter_result_none.append(row['code'])
        log.info(filter_result_none)
        log.info('Total:'+str(len(filter_result)+len(filter_result_none)))
        today=datetime.date.today()
        file_object_path = 'vipdoc/result/' + today.strftime('%Y-%m-%d') +'.txt'
        file_object = open(file_object_path, 'w+')
        file_object.writelines(','.join(filter_result))

# get_today_stock_data()
get_result_from_db()