import model
import numpy as np

def getAllData(start,rows):
    _list = model.select('trade',limit=str(start)+','+str(rows))
    step = 10
    tmpList = []
    for row in _list:
        if row[0]%step==1:
            amount = 0
            start_time = row[2]
            buy = 0
            start_price = row[4]

        amount+=row[1]
        buy+=row[3]
        if(row[0]%step)==0:
            #成交量，时间，买入占比，价格涨跌，价变速度
            tmpList.append([amount,(row[2]-start_time)*1.0/1000,buy*1.0/step,(row[4]-start_price)*1.0/start_price,(row[4]-start_price)*1.0/max(1,(row[2]-start_time))*1000])
    y_data = []
    x_data = []
    for key,row in enumerate(tmpList):
        if (key+2) > len(tmpList):
            break
        x_data.append(row)
        if tmpList[key+1][3]>0:
            y_data.append([1,0])
        else:
            y_data.append([0,1])
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    return x_data,y_data

