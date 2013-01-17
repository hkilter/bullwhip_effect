#libraries
library(forecast)

#rewrite to be iterable over all csv files

#scan list
setwd("C:\\Documents and Settings\\Luke\\Desktop\\community_test")

countries <- read.csv("country_tipping_points.txt", sep=",", header=FALSE)
countries_list <- countries$V1

setwd("C:\\Documents and Settings\\Luke\\Desktop\\bullwhipped\\out")

#note: need to throw out companies with no test data
for (i in 1:length(countries_list)) {
  #initilize country
  country <- countries_list[i]
  
  #read in the training and test sets
  dbtype1 <-"_train.csv"
  train <- paste(countries_list[i],dbtype1,sep="")
  train1 <- read.csv(train, sep=",", header=FALSE)
      #sort the set by year
      trainind <- order(train1$V1)
      foo <- train1$V1[trainind]
      bar <- train1$V2[trainind]
  
  #create time series object
  train_sorted <- data.frame(year=foo,usage_pct=bar)
  train_sorted.ts <- ts(train_sorted$usage_pct, frequency=1, start = train_sorted$year[1])
  
  #read in the test set
  dbtype2 <-"_test.csv"
  test  <- paste(countries_list[i],dbtype2,sep="")
  test1  <- read.csv(test, sep=",", header=FALSE)
      #sort into a data frame by year
      testind <- order(test1$V1)
      foo2 <- test1$V1[testind]
      bar2 <- test1$V2[testind]
  
  #create test object
  test_sorted <- data.frame(year=foo2,usage_pct=bar2)
  test_sorted.ts <- ts(test_sorted$usage_pct, frequency=1, start = test_sorted$year[1])
  
  #set length of available data
  forecast_length = length(bar2)
  max_value = test_sorted$usage_pct[forecast_length]+5
  
  #Plot training and test forecasts
  plot(forecast(train_sorted.ts, h=forecast_length), main=country, xlab="Year", ylab ="Percent Adopted", ylim=c(0,max_value))
  lines(test_sorted.ts, type ="l", col=1)
  
  #need to fix legend
  legend("topleft",legend=c("Best Fit","Actual"),col=0:1, lty=1,inset=.02)
  
  #accuracy
  fcast1 <- forecast(train_sorted.ts, h=forecast_length)
  fcast_accurarcy <-accuracy(fcast1, test_sorted.ts)
  
  #write the forecast accuracy to a file
  #write a png image to a file
}