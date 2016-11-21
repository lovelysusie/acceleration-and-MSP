library(dplyr)
library(data.table)
library(psd)


senser <-read.csv(file.choose())

#delet unused columns
senser <-senser[,-(9:12)]
head(senser)
table(senser$events)

senser<-data.frame(senser)
senser$accl <-sqrt(senser$accelerometerX^2+senser$accelerometerY^2+senser$accelerometerZ^2)
head(senser$accl)

######################
#without drift cancelation
acceleration <-aggregate(senser$accl,list(senser$ReadableTime), max)

matching <-data.frame(senser$ReadableTime,senser$PD3)
matching <-matching[!duplicated(matching$senser.ReadableTime), ]
acceleration <-cbind(acceleration,matching)
acceleration <-acceleration[,-3]
names(acceleration)<-c("time","max acceleration","PD3")
#############
table(senser$symptoms)
matching <-data.frame(senser$ReadableTime,senser$symptoms)
matching <-matching[!duplicated(matching$senser.ReadableTime), ]
#matching <-matching[-341,]
acceleration <-cbind(acceleration,matching)
acceleration <-acceleration[,-4]
names(acceleration)[4]<-"main symptons"
#############
matching <-aggregate(senser$accl,list(senser$ReadableTime), mean)
acceleration <-cbind(acceleration,matching)
acceleration <-acceleration[,-5]
names(acceleration)[5]<-"mean acceleration"
#############
i=1
series <-filter(senser,senser$ReadableTime==acceleration$time[i]|
                  senser$ReadableTime==acceleration$time[i+1])
series <-data.frame(mean(series$accl),max(series$accl))
series1 <-series

#######
i=3
j=nrow(acceleration)+1
while (i<j) {
  series <-filter(senser,senser$ReadableTime==acceleration$time[i]|
                    senser$ReadableTime==acceleration$time[i+1])
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

fun1 <-function(x) {
  x <-pspectrum(x$accelerometerX, x.frqsamp=62*2, niter = 1)
  x <-data.frame(freq=x$freq,spec=x$spec)
  x <-filter(x, x$freq>0.2 & x$freq<4)
  x <-mean(x$spec)
}

i=1
df <-filter(senser,senser$ReadableTime==acceleration$time[i]|
              senser$ReadableTime==acceleration$time[i+1])
df <-data.frame(MSP=fun1(df))
df1 <-df
#######
i=3
j=nrow(acceleration)+1
while (i<j) {
  df <-filter(senser,senser$ReadableTime==acceleration$time[i]|
                senser$ReadableTime==acceleration$time[i+1])
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
