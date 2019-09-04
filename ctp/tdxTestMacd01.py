import pandas as pd
import numpy as np
import datetime
import time
#获取数据
import os  
from color_log import Logger

#日志
log = Logger()


 
"""
根据 macd 是否在0 轴附近 ，筛选出个股， 出现突破进行买入持有 
"""



def get_EMA(df,N):   
    for i in range(len(df)):      
        if i==0:            
            df.ix[i,'ema']=df.ix[i,'close']        
        if i>0 :            
            df.ix[i,'ema']=(2*df.ix[i,'close']+(N-1)*df.ix[i-1,'ema'])/(N+1)
    ema=list(df['ema'])    
    
    return ema
def get_MACD(df,short=12,long=26,M=9):
    if len(df) < 28 :
        return 1
        
    a=get_EMA(df,short)    
    b=get_EMA(df,long)    
    df['diff']=pd.Series(a)-pd.Series(b)
    for i in range(len(df)):        
        if i==0:            
            df.ix[i,'dea']=df.ix[i,'diff']        
        if i>0:            
            df.ix[i,'dea']=(2*df.ix[i,'diff']+(M-1)*df.ix[i-1,'dea'])/(M+1)    
        df['macd']=2*(df['diff']-df['dea'])   

    diff1 =df.ix[i,'diff']
    dif1=round(diff1,3)
    diff2 =df.ix[i-1,'diff']
    dif2=round(diff2,3)
    vo1= df.ix[i,'volume']
    vo2= df.ix[i-1,'volume']
    
    close1= df.ix[i,'close']
    close2= df.ix[i-1,'close']

    if dif1 > dif2 and dif1 < 0.06 and dif1 > -0.06 and vo1 > vo2 and close1 > close2 :
        return dif1
    else :
        return 1


def set_df(code):
    df=pd.read_csv('C:/zd_zsone/vipdoc/szshdata/'+code+'.csv',encoding='gbk')
    df.columns=['date','open','high','low','close','volume']
    df=df[['date','open','high','low','close','volume']]
    df.head()
    return df


def file_name(file_dir):   
        L=[]   
        for root, dirs, files in os.walk(file_dir):  
            for file in files:  
                if os.path.splitext(file)[1] == '.csv':  
                    L.append(file)  
            return L


list1=file_name('C:/zd_zsone/vipdoc/szshdata/')

for i in list1:
    code=i[0:8]
    diff=get_MACD(set_df(code),12,26,9)
    if diff != 1 :
        log.info(code)
       # log.info(diff)
   