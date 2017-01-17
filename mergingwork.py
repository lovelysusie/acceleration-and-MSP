import pandas as pd

# if the file is 12HRS, run the code below:


sensorData = pd.read_csv("/Users/Susie/Documents/acceleration-and-MSP/PT17.0007.csv")
# loading data
sensorData['ReadableTime'] = pd.to_datetime(sensorData['time'], unit='ms')
# convert unix time to readable time
sensorData['ReadableTime'] = sensorData['ReadableTime'].apply(lambda x: x.strftime('%H:%M'))
# revise the time type

clinicalData = pd.read_excel("PT17.0007.xlsx", sheetname=1,header=0)
clinicalData['time'] = clinicalData['time'].apply(lambda x: x.strftime('%H:%M'))
clinicalData.rename(columns={'time': 'ReadableTime'}, inplace=True)
# change the columns name for mergering work

result = pd.merge(sensorData, clinicalData, how='left', on=['ReadableTime'])
print(result.head(5))

result.to_csv('PT17.0007_M.csv', index=False)
print(result.head(5))
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

i = 3
n = clinicalData.__len__()+1
while (i < n):
   dataFrame = sensorData[(sensorData['timeInSecond'] > clinicalData.at[i, 'UNIX-Time']) &
           (sensorData['timeInSecond'] < clinicalData.at[i+1, 'UNIX-Time'])]
   dataFrame['timeGroup'] = clinicalData.at[i, 'UNIX-Time']
   k = dataFrame.__len__()
   sensorData.at[j+1:j+k+1,'timeInSecond'] = dataFrame['timeGroup']
   j = j+k
   i = i + 1

clinicalData['timeInSecond'] = clinicalData['UNIX-Time']
result = pd.merge(sensorData, clinicalData, how='left', on=['timeInSecond'])
result.to_csv('PT17.0105_M.csv', index=False)
'''
