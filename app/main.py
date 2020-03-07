import tushare as ts
import datetime
import sys
import pandas as pd
import os
from color_log import Logger
from utils import Stock
import time

#日志
log = Logger()
stock=Stock()

#res = ts.get_hist_data('601860')
#print(res)

# 把沪深两的二进制文件转换成csv文件
def swap_file_to_csv():
    folders = ['sh','sz']
    for folder in folders:
        shsz = folder
        path = 'vipdoc/'+ shsz +'/lday/'
        listfile = os.listdir(path)
        for i in listfile:
            print(i)
            data = stock.read_tdx_lday_file(path+i)
            code=i.replace('.day','')
            data.to_csv(path_or_buf="vipdoc/szshdata/"+code+".csv",header=True)

# 过滤所有股票代码
def filter_code(isRealTime=False):
    fileList=[]
    filePath="vipdoc/szshdata/"
    filter_result=[]
    filter_result_none=[]
    # 停牌
    filter_result_stop=[]
    for root, dirs, files in os.walk(filePath):
        files.sort()
        for f in files:
            if os.path.splitext(f)[1] == '.csv':
                fileList.append(f)
    for i in fileList:
        code=i[0:8]
        _code=i[2:8]
        df=pd.read_csv(filePath+code+'.csv',encoding='gbk')
        # df.drop([len(df)-1],inplace=True)
        if isRealTime:
            cur_real_df = ts.get_realtime_quotes(_code)
            # 考虑停牌的情况
            if (float(cur_real_df['open'])==0):
                filter_result_stop.append(_code)
                continue
            inser_row = stock.get_insert_row(cur_real_df)
            df_append = pd.DataFrame(inser_row, index=[len(df)])
            df = df.append(df_append)
        diff=stock.get_MACD(df,12,26,9)
        if diff != 1 :
            filter_result.append(_code)
            log.info(code)
        else :
            filter_result_none.append(_code)
    # log.info(filter_result_none)
    if(len(filter_result_stop)>0):
        log.info('Stop:'+','.join(filter_result_stop))
    log.info('Total:'+str(len(filter_result)+len(filter_result_none)))
    today=datetime.date.today()
    real_file=''
    if isRealTime:
        real_file='-r-'
    file_object_path = 'vipdoc/result/' + today.strftime('%Y-%m-%d')+ real_file +'.txt'
    file_object = open(file_object_path, 'w+')
    file_object.writelines(','.join(filter_result))
# 程序入口
def main():
    # 执行生成csv文件
    # swap_file_to_csv()
    filter_code(isRealTime=False)

main()