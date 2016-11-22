import pandas as pd
from dateutil import parser
from scipy.signal import butter,lfilter
import matplotlib.pyplot as plt
from scipy import signal

'''
sensorData = pd.read_csv("/Volumes/HAONAN/1.raw data/PT17.0105_M.csv", low_memory=False)
grouped = sensorData.groupby(pd.TimeGrouper('60S'))
'''   
pd.set_option("display.max_rows",500)

def loadData():
    sensorData = pd.read_csv("/Volumes/HAONAN/1.raw data/PT17.0105_M.csv", low_memory=False)
    sensorData['ReadableTime'] = pd.to_datetime(sensorData['time'], unit='ms')
    sensorData['ReadableTime'] = sensorData['ReadableTime'].apply(lambda x: x.strftime('%H:%M:%S'))
    return sensorData
#pd3 RT BK Gait FOG
def groupData(sensorData):
    #sensorData = sensorData.set_index(sensorData['sensorTime.s.'].map(parser.parse))
    sensorData = sensorData.set_index(sensorData['ReadableTime'].map(parser.parse))
    grouped = sensorData.groupby(pd.TimeGrouper('60S'))
    return grouped

def butterBandPass(lowcut,highcut,fs,order=5):
    nyq = fs*0.5
    low = lowcut/nyq
    high = highcut/nyq
    b,a = butter(order,[low, high], btype='bandpass')
    return b,a

def butterBandPassFilter(data,lowcut,highcut,fs,order):
    b,a = butterBandPass(lowcut,highcut,fs,order=order)
    y = lfilter(b,a,data)
    return y

def powerSpectralDensity(data,fs):
    f,psd = signal.periodogram(data,fs,scaling="spectrum",return_onesided=True)
    return f,psd
#dramwing a raw periodogram
'''  
y = [i for i in grouped]
Fs = 67*2
f1,accx = signal.periodogram(y,fs=Fs,scaling='density',return_onesided=True)
plt.subplot(211)
plt.plot(f1,accx)
'''

def powerSpectralWelch(data,fs,cnt):
    f,psd = signal.welch(data,fs,'hanning',scaling='spectrum',nfft=cnt,noverlap=cnt/2,nperseg=cnt,return_onesided=True)
    return f,psd

def dominatFrequencyClac(psdData):
    maxX = max(psdData['psdX'])
    maxY = max(psdData['psdY'])
    maxZ = max(psdData['psdZ'])
    sumX = sum(psdData['psdX'])
    sumY = sum(psdData['psdY'])
    sumZ = sum(psdData['psdZ'])
    indexX = psdData[psdData['psdX'] == maxX].index.tolist()[0]
    #print("index",int(indexX),"+",indexX)
    indexY = psdData[psdData['psdY'] == maxY].index.tolist()[0]
    indexZ = psdData[psdData['psdZ'] == maxZ].index.tolist()[0]
    fX = psdData.get_value(indexX,'f')
    fY = psdData.get_value(indexY,'f')
    fZ = psdData.get_value(indexZ,'f')

    indexX1 = indexX+1
    indexX2 = indexX-1
    #print(indexX1,indexX,indexX2)
    #print("valeu",psdData.get_value(indexX1,'psdX'))
    if indexX>1:
        peakX = psdData.get_value(indexX+1,'psdX')+psdData.get_value(indexX,'psdX')+psdData.get_value(indexX-1,'psdX')
    else:
        peakX = maxX
    if indexY>1:
        peakY = psdData.get_value(indexY+1,'psdY')+psdData.get_value(indexY,'psdY')+psdData.get_value(indexY-1,'psdY')
    else:
        peakY = maxY
    if indexZ>1:
        peakZ = psdData.get_value(indexZ+1,'psdZ')+psdData.get_value(indexZ,'psdZ')+psdData.get_value(indexZ-1,'psdZ')
    else:
        peakZ = maxZ
    #print(peakX,peakY,peakZ)

    if(maxX == max(maxX,maxY,maxZ)):
       return fX,maxX,sumX,indexX,peakX
    elif(maxY == max(maxX,maxY,maxZ)):
        return fY,maxY,sumY,indexY,peakY
    else:
        return fZ,maxZ,sumZ,indexZ,peakZ


lowcut = 3
highcut = 12
fs = 64
order =2
sensorData = loadData()
grouped = groupData(sensorData)

i = 1
finalDF = pd.DataFrame()
for time,group in grouped:
    if not group.empty:
        print('time',time)
        cnt = group['accelerometerX'].count()
        #print("count",cnt)
        #everySecond = group.groupby(pd.TimeGrouper('1S'))
        restTremorValue = group['RT'].mean()
        #print(restTremorValue)
        #print(type(group['accelerometerX']))
        '''
        bpData = group.groupby(pd.TimeGrouper('1S'))
        for bpTime,bpGroup in bpData:
            if not bpGroup.empty:
                oneAX = butterBandPassFilter(bpGroup['accelerometerX'],lowcut,highcut,fs*2,order=6)
                tenAX += oneAX
        '''
        ay = butterBandPassFilter(group['accelerometerY'], lowcut, highcut, fs, order)
        #print(ay)
        ax = butterBandPassFilter(group['accelerometerX'],lowcut,highcut,fs,order)
        #print(ax)
        az = butterBandPassFilter(group['accelerometerZ'],lowcut,highcut,fs,order)
        gx = butterBandPassFilter(group['gyroscopeX'],lowcut,highcut,fs,order)
        gy = butterBandPassFilter(group['gyroscopeY'],lowcut,highcut,fs,order)
        gz = butterBandPassFilter(group['gyroscopeZ'],lowcut,highcut,fs,order)

        fax,psdax = powerSpectralDensity(ax,fs)
        #print(fax,psdax)
        fay,psday = powerSpectralDensity(ay,fs)
        faz,psdaz = powerSpectralDensity(az,fs)
        fgx,psdgx = powerSpectralDensity(gx,fs)
        fgy,psdgy = powerSpectralDensity(gy,fs)
        fgz,psdgz = powerSpectralDensity(gz,fs)
        '''
        fax, psdax = powerSpectralWelch(ax, fs * 2,cnt)
        fay, psday = powerSpectralWelch(ay, fs * 2,cnt)
        faz, psdaz = powerSpectralWelch(az, fs * 2,cnt)
        fgx, psdgx = powerSpectralWelch(gx, fs * 2,cnt)
        fgy, psdgy = powerSpectralWelch(gy, fs * 2,cnt)
        fgz, psdgz = powerSpectralWelch(gz, fs * 2,cnt)
        '''
        accPsdDf = pd.DataFrame({'f':fax,'psdX':psdax,'psdY':psday,'psdZ':psdaz})
        gyroPsdDf = pd.DataFrame({'f':fax,'psdX':psdgx,'psdY':psdgy,'psdZ':psdgz})
        aDF,aPower,aSum,aIndex,aPeak = dominatFrequencyClac(accPsdDf)
        gDF,gPower,gSum,gIndex,gPeak = dominatFrequencyClac(gyroPsdDf)
        totalMax = max(aPower,gPower)
        #print("acc",aDF,aPower,aIndex)
        #print("gyro",gDF,gPower,gIndex)
        aPer = (aPeak/(aSum-aPeak))*100
        gPer = (gPeak/(gSum-gPeak))*100
        tPer = (totalMax/(aSum+gSum))*100
        #finalDF.append({'aDF':aDF,'aPower':aPower,'aPer':aPer,'gDF':gDF,'gPower':gPower,'gPer':gPer,'restTremorValue':restTremorValue},ignore_index=True)
        #finalDF.append(np.array(aDF,aPower,aPer,gDF,gPower,gPer,restTremorValue))
        finalDF.loc[i,'aDF']=aDF
        finalDF.loc[i,'aPower'] = aPower
        finalDF.loc[i,'aPer'] = aPer
        finalDF.loc[i,'gDF'] = gDF
        finalDF.loc[i,'gPower'] = gPower
        finalDF.loc[i,'gPer'] = gPer
        finalDF.loc[i,'tPer'] = tPer
        finalDF.loc[i,'time'] = time
        finalDF.loc[i,'restTremorValue'] = restTremorValue
        i += 1
        if False:
        #if restTremorValue < 2:
            plt.subplot(321)
            plt.plot(fax,psdax)
            plt.title("accelorometerX")
            plt.subplot(322)
            plt.plot(fay,psday)
            plt.title("accelorometerY")
            plt.subplot(323)
            plt.plot(faz,psdaz)
            plt.title("accelorometerZ")
            plt.subplot(324)
            plt.plot(fgx,psdgx)
            plt.title("gyroscopeX")
            plt.subplot(325)
            plt.plot(fgy,psdgy)
            plt.title("gyroscopeY")
            plt.subplot(326)
            plt.plot(fgz,psdgz)
            plt.title("gyroscopeZ")
            plt.tight_layout()

            filePath = ""
            time_file_name = str(time).strip()
            time_array = time_file_name.split(" ")
            fileName = time_array[1].replace(":","-")


            filePath = "E:\\Internship\\Merged data\\Images\\testbandpass\\NT2\\"+str(round(restTremorValue))+"_"+fileName+".png"
            #plt.savefig(filePath)
            #else:
            #filePath = "E:\\Internship\\Merged data\\Images\\welch\\NonTremor\\" + fileName + ".png"

            plt.savefig(filePath)
            plt.clf()
            #print(psdDf)
            #print(finalDF)
#plt.plot(finalDF['aPower'])
#plt.fill(finalDF['restTremorValue'],alpha=0.2)
#plt.show()
finalDF.to_csv("E:/Internship/Merged data/Results/normal_activity_tremor.csv")
'''
maxX = max(accPsdDf['psdx'])
print("maxX",maxX)
indexX =accPsdDf[accPsdDf['psdx']==maxX].index.tolist()[0]

print("indexX",indexX)
print("power",accPsdDf.get_value(indexX,'psdax'))
print("f",accPsdDf.get_value(indexX,'f'))
'''


    #plt.plot(fax,psdax)
    #print("after", ax)
    #print('frequencyx',fx)
    #print('psdx',psdx)
    #plt.plot(group['accelerometerX'])
    #plt.plot(ax,label="x")
    #plt.plot(df1['x'],label="rawx")
    #plt.plot(ay,label="y")
    #plt.plot(az,label="z")
    #plt.show()
    #print('hi')

#