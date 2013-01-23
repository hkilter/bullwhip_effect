#libraries
library(forecast)

#rewrite to be iterable over all csv files

#scan list
setwd("C:\\Documents and Settings\\Luke\\Desktop\\community_test")

countries <- read.csv("country_tipping_points.txt", sep=",", header=FALSE)
countries_list <- countries$V1

#use p and q from recommendation
p_data = .05
q_data = .33

setwd("C:\\Documents and Settings\\Luke\\Desktop\\bullwhipped\\out")

#create data frame to write file to
N <- length(countries_list)

#need a table with: country, year, best_fit_projection, bass_projection. 
#from pre 6.67% sample
summary <- data.frame(countries_list=rep("", N), stringsAsFactors=FALSE)

#note: need to throw out companies with no test data
for (i in 1:length(countries_list)) {
  #initilize country
  country <- countries_list[i]
  
  #read in the training and test sets
  dbtype1 <-"_train.csv"
  train <- paste(country,dbtype1,sep="")
  train1 <- try(read.csv(train, sep=',', quote="\'", header=FALSE));
      if(class(train1) == "try-error") next;
  
      #sort the set by year
      trainind <- order(train1$V1)
      foo <- train1$V1[trainind]
      bar <- train1$V2[trainind]
  
  #create time series object
  train_sorted <- data.frame(year=foo,usage_pct=bar)
  train_sorted.ts <- ts(train_sorted$usage_pct, frequency=1, start = train_sorted$year[1])
  
  #read in the test set
  dbtype2 <-"_test.csv"
  test  <- paste(country,dbtype2,sep="")
  test1 <- try(read.csv(test, sep=',', quote="\'", header=FALSE));
      if(class(test1) == "try-error") next;
  
      #sort into a data frame by year
      testind <- order(test1$V1)
      foo2 <- test1$V1[testind]
      bar2 <- test1$V2[testind]
  
  #create test object and sort the time series by year
  test_sorted <- data.frame(year=foo2,usage_pct=bar2)
  test_sorted.ts <- ts(test_sorted$usage_pct, frequency=1, start = test_sorted$year[1])
  
  #set length of available data
  forecast_length = length(bar2)
  max_value = test_sorted$usage_pct[forecast_length]+30
  
  #***START BASS MODEL***
  T79 <- 1: forecast_length
  #project 10 years time
  Tdelt <- (1:100) / forecast_length
  
  #adoption
  Sales <- test_sorted$usage_pct
  series_length <- length(Sales)
  population <- Sales[series_length]
  Cusales <- cumsum(Sales)
  
  m <- 50 * (forecast_length/10)
  p <- p_data
  q <- q_data
  
  # setting the starting value for M to the recorded total sales.
  ngete <- exp(-(p+q) * Tdelt)
  
  # find Bass probability density function and continuous density function
  Bpdf <- m * ( (p+q)^2 / p ) * ngete / (1 + (q/p) * ngete)^2
  Bcdf <- m * (1 - ngete)/(1 + (q/p)*ngete)
  #plot(Tdelt, Bcdf, xlab = "Years", ylab = "Cumulative Adoption", type='l')
  
  times <- c(10,20,30,40,50,60,79,80,90,100)
  N <- forecast_length
  
  bass_plot<- data.frame(year=rep(NA, N), bass_pct=rep(NA, N), stringsAsFactors=FALSE)
  for(i in 1:forecast_length) {
      bass_plot[i,] <- data.frame(year=test_sorted$year[i],bass_pct=Bcdf[times[i]])
  }
  

  bass_sorted.ts <- ts(bass_plot$bass_pct, frequency=1, start = bass_plot$year[1])
  
  #Plot training set and plot bass and best-fit forecast. Save plot. 
  
  plot_type <- "_diffusion_plot.png"      
  plot_save  <- paste(country,plot_type,sep="")
  png(plot_save)
  plot(forecast(train_sorted.ts, h=forecast_length), main=country, xlab="Year", ylab ="Percent Adopted", ylim=c(0,max_value))
  lines(test_sorted.ts, type ="l", col=2)
  lines(bass_sorted.ts, type="l", col=8)
  dev.off()
  
  #need to fix legend
  #legend("topleft",legend=c("Best Fit","Actual"),col=0:1, lty=1,inset=.02)
  
  #accuracy
  #fcast1 <- forecast(train_sorted.ts, h=forecast_length)
  #fcast_accurarcy <-accuracy(fcast1, test_sorted.ts)
  
  #write the forecast accuracy to a file
  #summary[i, ] <- c(countries_list[i])
  #write a png image to a file
}