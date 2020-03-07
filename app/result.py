import sys
import os


#res = ts.get_hist_data('601860')
#print(res)

# df = ts.get_realtime_quotes('600008') #Single stock symbol
# df[['code','name','price','bid','ask','volume','amount','time']]
# print(df)


# 求历史结果的交集

def query_result_intersection():
    filePath="vipdoc/result/"
    filter_result=[]
    for root, dirs, files in os.walk(filePath):
        files.sort()
        for f in files:
            date_name = os.path.splitext(f)[0]
            file_object = open(filePath+f, 'r')
            res=file_object.read()
            filter_result.append({"date":date_name,"result":res.split(',')})
            file_object.close()

    temp_name=''
    temp_result=[]
    print('============= Today & Yesterday =============')
    for item in filter_result:
        if len(temp_result)>0:
            print(temp_name+' + '+item['date']+' : ')
            inter = list(set(temp_result) & set(item['result']))
            print(','.join(inter))
        temp_name=item['date']
        temp_result=item['result']

    print('============= Today & Before =============')
    last=filter_result.pop()
    temp_name=last['date']
    temp_result=last['result']
    for i in filter_result:
        print(temp_name+' + '+i['date']+' : ')
        inter2 = list(set(temp_result) & set(i['result']))
        print(','.join(inter2))
    
    print('============= Recent three days intersection =============')
    last_2=filter_result.pop()
    last_3=filter_result.pop()
    inter3= list(set(last['result']) & set(last_2['result']) & set(last_3['result']))
    print(','.join(inter3))
        
# 查询交集结果
query_result_intersection()