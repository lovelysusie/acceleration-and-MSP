import pandas as pd

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
