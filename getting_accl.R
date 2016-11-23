library(dplyr)
library(data.table)
library(psd)
library(signal)
library(ggplot2)

sensor <-read.csv(file.choose())

#delet unused columns
sensor <-sensor[,-(9:12)]
head(sensor)
table(sensor$events)

sensor<-data.frame(sensor)
sensor$accl <-sqrt(sensor$accelerometerX^2+sensor$accelerometerY^2+sensor$accelerometerZ^2)
head(sensor$accl)

######################
#without drift cancelation
acceleration <-aggregate(sensor$accl,list(sensor$ReadableTime), max)

matching <-data.frame(sensor$ReadableTime,sensor$PD3)
matching <-matching[!duplicated(matching$sensor.ReadableTime), ]
acceleration <-cbind(acceleration,matching)
acceleration <-acceleration[,-3]
names(acceleration)<-c("time","max acceleration","PD3")
#############
table(sensor$symptoms)
matching <-data.frame(sensor$ReadableTime,sensor$symptoms)
matching <-matching[!duplicated(matching$sensor.ReadableTime), ]
#matching <-matching[-341,]
acceleration <-cbind(acceleration,matching)
acceleration <-acceleration[,-4]
names(acceleration)[4]<-"main symptons"
#############
matching <-aggregate(sensor$accl,list(sensor$ReadableTime), mean)
acceleration <-cbind(acceleration,matching)
acceleration <-acceleration[,-5]
names(acceleration)[5]<-"mean acceleration"
#############
i=1
series <-filter(sensor,sensor$ReadableTime==acceleration$time[i]|
                  sensor$ReadableTime==acceleration$time[i+1])
series <-data.frame(mean(series$accl),max(series$accl))
series1 <-series

#######
i=3
j=nrow(acceleration)+1
while (i<j) {
  series <-filter(sensor,sensor$ReadableTime==acceleration$time[i]|
                    sensor$ReadableTime==acceleration$time[i+1])
  series <-data.frame(mean(series$accl),max(series$accl))
  series1 <-rbind(series1,series)
  i=i+2
}
#######
del <- seq(2, nrow(acceleration), by = 2)
acceleration[-del,]
series1 <-cbind(series1,acceleration[-del,])
series1 <-series1[,-4]
series1 <-series1[,-6]
names(series1)[1:2] <-c("mean", "max")
#######
names(acceleration) <-c("time","accl")

bandpassfilter <-butter(n=6, W=c(0.2/62,4/62),type="pass")

fun1 <-function(x) {
  x =filter(bandpassfilter, x$accelerometerX)
  x =c(x)
  x =pspectrum(x, x.frqsamp=62*2, niter = 1)
  x =data.frame(freq=x$freq,spec=x$spec)
  x =data.table(x)
  x =x[freq>0.2 & freq<4]
  x <-mean(x$spec)
}

i=1
df <-filter(sensor,sensor$ReadableTime==acceleration$time[i]|
              sensor$ReadableTime==acceleration$time[i+1])
df <-data.frame(MSP=fun1(df))
df1 <-df
#######
i=3
j=nrow(acceleration)+1
while (i<j) {
  df <-filter(sensor,sensor$ReadableTime==acceleration$time[i]|
                sensor$ReadableTime==acceleration$time[i+1])
  df <-data.frame(MSP=fun1(df))
  df1 <-rbind(df1,df)
  i=i+2
}

del <-seq(2,340,by=2)
series1 <-acceleration[-del,]
series1 <-cbind(series1,df1)
series1 <-series1[,-2]
healthy <-read.csv(file.choose())
mean(healthy$MSP)
mean(series1$MSP)

##########################
setwd("/Users/Susie/Desktop")
write.csv(series1, "PT.0007_MSP_b.csv", row.names = FALSE)
