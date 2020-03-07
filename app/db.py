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
    count_array = []
    filter_result_stop = []
    for index, row in df_read.iterrows():
        cur_real_df = ts.get_realtime_quotes(row['code'])
        # 考虑停牌的情况
        if (float(cur_real_df['open'])==0):
            filter_result_stop.append(row['code'])
            continue
        today_date = cur_real_df.loc[0,'date']
        # cur_query = 'select * from `' + row['table_name'] +"` where date in ('" + today_date +"');"
        cur_df = pd.read_sql_query('select * from '+row['table_name'],engine)
        find_res = cur_df.loc[cur_df['date'] == today_date].head()
        if len(find_res) == 0:
            inser_row = stock.get_insert_row(cur_real_df)
            print('Insert today data ==> '+row['code'])
            df_write = pd.DataFrame(inser_row, index=[len(cur_df)])
            df_write.to_sql(row['table_name'], engine, index=False, if_exists='append')
        else :
            count_array.append(row['code'])
            
    if(len(filter_result_stop)>0):
        log.info('Stop:'+','.join(filter_result_stop))
    log.info('Pass:'+str(len(count_array)))


# 一次性获取所有今天股票实时数据并更新数据库
def get_today_stock_data2():
    today_all=ts.get_today_all()
    df = pd.DataFrame(today_all)
    for index, row in df.iterrows():
        print(row)
        break

# 从数据库中读取数据并算出结果
def get_result_from_db(realtime=False,date=''):
    sql_query = 'select * from stocks;'
    # 使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
    df_read = pd.read_sql_query(sql_query, engine)
    filter_result = []
    filter_result_none=[]
    filter_result_stop = []
    for i in range(len(df_read)):
        sql_table='select * from '+df_read.loc[i,'table_name']
        if date!='':
            sql_table=sql_table+' where `date` <= "'+date+'"'
        df = pd.read_sql_query(sql_table, engine)
        if realtime and date=='':
            cur_real_df = ts.get_realtime_quotes(df_read.loc[i,'code'])
            # 考虑停牌的情况
            if (float(cur_real_df['open'])==0):
                filter_result_stop.append(df_read.loc[i,'code'])
                continue
            inser_row = stock.get_insert_row(cur_real_df)
            df_append = pd.DataFrame(inser_row, index=[len(df)])
            df = df.append(df_append)
        diff=stock.get_MACD(df,12,26,9)
        if diff != 1 :
            filter_result.append(df_read.loc[i,'code'])
            log.info(df_read.loc[i,'table_name'])
        else :
            filter_result_none.append(df_read.loc[i,'code'])
    if(len(filter_result_stop)>0):
        log.info('Stop:'+','.join(filter_result_stop))
    log.info('Total:'+str(len(filter_result)+len(filter_result_none)))
    today=datetime.date.today()
    real_file=''
    if realtime and date=='':
        real_file='-r-'
    file_object_path = 'vipdoc/result/' + today.strftime('%Y-%m-%d') + real_file +'.txt'
    file_object = open(file_object_path, 'w+')
    file_object.writelines(','.join(filter_result))

# get_today_stock_data()
get_result_from_db(date='2020-03-04')