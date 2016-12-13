import pandas as pd
import numpy as np
# if the file is 12HRS, run the code below:

'''
sensorData = pd.read_csv("/Users/Susie/Documents/patientdata0016/PT17.0016.csv",low_memory=True)
# loading data
sensorData['ReadableTime'] = pd.to_datetime(sensorData['time'], unit='ms')
# convert unix time to readable time
sensorData['ReadableTime'] = sensorData['ReadableTime'].apply(lambda x: x.strftime('%H:%M'))
# revise the time type

clinicalData = pd.read_excel("/Users/Susie/Documents/patientdata0016/PT17.0016.xlsx", sheetname=1,header=0)
clinicalData['time'] = clinicalData['time'].apply(lambda x: x.strftime('%H:%M'))
clinicalData.rename(columns={'time': 'ReadableTime'}, inplace=True)
# change the columns name for mergering work

result = pd.merge(sensorData, clinicalData, how='left', on=['ReadableTime'])
print(result.head(5))

result.to_csv('PT17.0016_M.csv', index=False)
'''

# if the file is 15 min, run the code below:
sensorData = pd.read_csv("/Users/Susie/Documents/PT17.0105/PT17.0105_01.csv",low_memory=True)
sensorData['timeInSecond'] = sensorData['time']/1000

clinicalData = pd.read_excel("/Users/Susie/Documents/PT17.0105/PT17.0105.xlsx", sheetname=1,header=0,
                             skiprows=5)
clinicalData = clinicalData[2:]

dataFrame = sensorData[(sensorData['timeInSecond'] > clinicalData.at[2, 'UNIX-Time']) &
           (sensorData['timeInSecond'] < clinicalData.at[3, 'UNIX-Time'])]
dataFrame['timeGroup'] = clinicalData.at[2, 'UNIX-Time']
j = dataFrame.__len__()
sensorData.at[1:j,'timeInSecond'] = dataFrame['timeGroup']

for time in clinicalData['UNIX-Time']:
    





print(sensorData.head(5))
