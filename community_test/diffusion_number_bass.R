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
N <- length(countries_list) * 15

#need a table with: country, year, best_fit_projection, bass_projection. 
#from pre 6.67% sample
summary <- data.frame(country_label=rep("", N), year=rep(NA, N), bass_pct=rep(NA, N), stringsAsFactors=FALSE)
summary_count = 1
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
  plus_five_years = forecast_length + 5
  
  #***START BASS MODEL***
  T79 <- 1: plus_five_years
  #project five years time
  Tdelt <- (1:100) / plus_five_years
  
  #adoption
  Sales <- test_sorted$usage_pct
  series_length <- length(Sales)
  population <- Sales[series_length]
  Cusales <- cumsum(Sales)
  
  #need to think about this attribute
  m <- 50 * (2) * log(forecast_length, plus_five_years)
  p <- p_data
  q <- q_data
  
  # setting the starting value for M to the recorded total sales.
  ngete <- exp(-(p+q) * Tdelt)
  
  # find Bass probability density function and continuous density function
  Bpdf <- m * ( (p+q)^2 / p ) * ngete / (1 + (q/p) * ngete)^2
  Bcdf <- m * (1 - ngete)/(1 + (q/p)*ngete)
  
  plot(Tdelt, Bcdf, xlab = "Years", ylab = "Cumulative Adoption", type='l')
  
  #divide a time range into forecast points
  N3 <- plus_five_years
  times <- data.frame(sample_point=rep(NA,N3), stringsAsFactors=FALSE)
  
  for(d in 1:plus_five_years) {
    point <- 100-(d-1)*(round(100/plus_five_years))
    times[d,] <- data.frame(sample_point=point)
  }
  
  bass_sort <- order(times$sample_point)
  bass_points <- times$sample_point[bass_sort]
  
  # make a time series with the sample forecast points
  N2 <- plus_five_years
  bass_plot<- data.frame(year=rep(NA, N2), bass_pct=rep(NA, N2), stringsAsFactors=FALSE)
  for(j in 1:plus_five_years) {
      
      projected_year <- test_sorted$year[1] + j - 1
      bass_plot[j,] <- data.frame(year=projected_year,bass_pct=Bcdf[bass_points[j]])
  }
  
  bass_sorted.ts <- ts(bass_plot$bass_pct, frequency=1, start = bass_plot$year[1])
  
  #***END BASS MODEL***
  
  #Plot training set and plot bass and best-fit forecast. Save plot. 
  #plot_type <- "_diffusion_plot.png"      
  #plot_save  <- paste(country,plot_type,sep="")
  #png(plot_save)
  #plot(forecast(train_sorted.ts, h=forecast_length), main=country, xlab="Year", ylab ="Percent Adopted", ylim=c(0,max_value))
  #lines(test_sorted.ts, type ="l", col=2)
  #lines(bass_sorted.ts, type="l", col=8)
  #dev.off()
  
  country_label  <- paste(country)
  #print a triplestore summary
  #k = 12 and krange = 18, l = {1, 2, 3, 4, 5, 6}
  
  for (l in 1:length(bass_plot$year)) {
     if(bass_plot$year[l] >= 2009) {
       summary[summary_count, ] <- c(country_label, bass_plot$year[l], bass_plot$bass_pct[l])
       summary_count = summary_count + 1
     } 
  }
}