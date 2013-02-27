Models of influence of money on gains

cloud <- read.csv("cloud_comp.csv", header=TRUE)

#linear models

cloud.lm <- lm(Revenue_millions~ volume + Score_100, data=cloud)

#graphs
p <- ggplot(cloud, aes(x =volume,y=Revenue_millions))
p + geom_point()
r <- ggplot(cloud, aes(x =Score_100,y=Revenue_millions))
r + geom_point()