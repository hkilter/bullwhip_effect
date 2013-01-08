#Telecom Network linear Model
library(ggplot2)
telecom <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\supplier_buyer_graph\\relationship_algorithms2.csv", sep=",", header=TRUE)

#linear model

telecom.lm <- lm(last_year_funds~starting_funds_millions+ Degree, data=telecom)

#graphs
p <- ggplot(telecom, aes(x =Degree,y=last_year_funds))
p + geom_point()
r <- ggplot(telecom, aes(x =Degreey=lasy_year_funds))
r + geom_point()