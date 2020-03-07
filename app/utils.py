import pandas as pd
import numpy as np
import datetime
import struct
import sys
import os

class Stock(object):
    # def __init__(self):
    
    def get_insert_row(self,data_frame,date=''):
        _date = data_frame.loc[0,'date']
        if date !='':
            _date=date
        inser_row = {
            'date':_date,
            'open':round(float(data_frame.loc[0,"open"]),2),
            'high':round(float(data_frame.loc[0,"high"]),2),
            'low':round(float(data_frame.loc[0,"low"]),2),
            'close':round(float(data_frame.loc[0,"price"]),2),
            'amount':round(float(data_frame.loc[0,"amount"]),1),
            'volume':int(data_frame.loc[0,"volume"])
        }
        return inser_row

    # 核心

    """
    根据 macd 是否在0 轴附近 ，筛选出个股， 出现突破进行买入持有 
    """

    def get_EMA(self,df,N):   
        for i in range(len(df)):      
            if i==0:            
                df.loc[i,'ema']=float(df.loc[i,'close'])        
            if i>0 :            
                df.loc[i,'ema']=(2*float(df.loc[i,'close'])+(N-1)*float(df.loc[i-1,'ema']))/(N+1)
        ema=list(df['ema'])
        return ema

    def get_MACD(self,df,short=12,long=26,M=9):
        if len(df) < 28 :
            return 1
            
        a=self.get_EMA(df,short)    
        b=self.get_EMA(df,long)
        df['diff']=pd.Series(a)-pd.Series(b)
        for i in range(len(df)):        
            if i==0:            
                df.loc[i,'dea']=df.loc[i,'diff']        
            if i>0:            
                df.loc[i,'dea']=(2*df.loc[i,'diff']+(M-1)*df.loc[i-1,'dea'])/(M+1)    
            df['macd']=2*(df['diff']-df['dea'])   

        diff1 =df.loc[i,'diff']
        dif1=round(diff1,3)
        diff2 =df.loc[i-1,'diff']
        dif2=round(diff2,3)
        vo1= df.loc[i,'volume']
        vo2= df.loc[i-1,'volume']
        
        close1= df.loc[i,'close']
        close2= df.loc[i-1,'close']

        if dif1 > dif2 and dif1 < 0.06 and dif1 > -0.06 and vo1 > vo2 and close1 > close2 :
            return dif1
        else :
            return 1

    def read_tdx_lday_file(self,codeFile=""):
        dataSet=[]
        with open(codeFile,'rb') as fl:
            buffer=fl.read()
            size=len(buffer)
            rowSize=32
            # code=os.path.basename(codeFile).replace('.day','')
            for i in range(0,size,rowSize):
                row=list(struct.unpack('IIIIIfII',buffer[i:i+rowSize]))
                date_format = datetime.datetime.strptime(str(row[0]),'%Y%M%d')
                row[0]=date_format.strftime('%Y-%M-%d')
                row[1]=str(row[1]/100)
                row[2]=str(row[2]/100.0)
                row[3]=str(row[3]/100.0)
                row[4]=str(row[4]/100.0)
                row[5]=str(row[5])
                row[6]=str(row[6])
                row.pop()
                dataSet.append(row)
        
        data=pd.DataFrame(data=dataSet,columns=['date','open','high','low','close','amount','volume'])
        return data