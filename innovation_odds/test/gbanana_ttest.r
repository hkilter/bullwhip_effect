#t-test
library(nutshell)
data(tires.sus)

#tire test
times.to.failure.e <- subset(tires.sus, Tire_Type=="E" & Speed_At_Failure_km_h==180)$Time_To_Failure
times.to.failure.d <- subset(tires.sus, Tire_Type=="D" & Speed_At_Failure_km_h==180)$Time_To_Failure
times.to.failure.b <- subset(tires.sus, Tire_Type=="B" & Speed_At_Failure_km_h==180)$Time_To_Failure

preint <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\test\\preinternet.csv", sep=",", header=TRUE)
postint <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\test\\postinternet.csv", sep=",", header=TRUE)

preint.superfast <- subset(preint, Time.to.50.million < 8)$Revenue.2008.millions
preint.fast <- subset(preint, Time.to.50.million > 7)$Revenue.2008.millions
postint.superfast <- subset(postint, Time.to.50.million < 5)$Revenue.2008.millions
postint.fast <- subset(postint, Time.to.50.million > 4)$Revenue.2008.millions

#subset 
set_percent <- gbanana$Over..500.million / gbanana$Total


gbanana2 <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\test\\gbanana_ttest2.csv", sep=",", header=TRUE)

revenues.a <- subset(gbanana2, Group=="A")$Revenue.2008.millions
revenues.b <- subset(gbanana2, Group=="B")$Revenue.2008.millions
revenues.c <- subset(gbanana2, Group=="C")$Revenue.2008.millions
revenues.d <- subset(gbanana2, Group=="D")$Revenue.2008.millions
revenues.e <- subset(gbanana2, Group=="E")$Revenue.2008.millions


wilcox.test(revenues.a, revenues.c)
wilcox.test(revenues.a, revenues.b)
wilcox.test(revenues.c, revenues.d)
wilcox.test(revenues.c, revenues.e)

wilcox.test(preint.superfast, preint.fast)
wilcox.test(postint.superfast, postint.fast)
