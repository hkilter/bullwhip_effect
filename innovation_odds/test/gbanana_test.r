#t-test
library(nutshell)


preint <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\test\\preinternet.csv", sep=",", header=TRUE)
postint <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\test\\postinternet.csv", sep=",", header=TRUE)
testset <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\test\\out_sample_test.csv", sep=",", header=TRUE)

preint.superfast <- subset(preint, Time.to.50.million < 8)$Revenue.2008.millions
preint.fast <- subset(preint, Time.to.50.million > 7)$Revenue.2008.millions
postint.superfast <- subset(postint, Time.to.50.million < 5)$Revenue.2008.millions
postint.fast <- subset(postint, Time.to.50.million > 4)$Revenue.2008.millions

testset.hot <- subset(testset, Time.to.50.million < 4)$Revenue_2011_millions
testset.fast <- subset(testset,  Time.to.50.million < 8 & Time.to.50.million > 4 )$Revenue_2011_millions


#subset 
set_percent <- gbanana$Over..500.million / gbanana$Total


gbanana2 <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\test\\gbanana_ttest2.csv", sep=",", header=TRUE)

revenues.a <- subset(gbanana2, Group=="A")$Revenue.2008.millions
revenues.b <- subset(gbanana2, Group=="B")$Revenue.2008.millions
revenues.c <- subset(gbanana2, Group=="C")$Revenue.2008.millions
revenues.d <- subset(gbanana2, Group=="D")$Revenue.2008.millions
revenues.e <- subset(gbanana2, Group=="E")$Revenue.2008.millions

revenues.c_test <- subset(testset, Group=="C")$Revenue_2011_millions
revenues.d_test<- subset(testset, Group=="D")$Revenue_2011_millions
revenues.e_test <- subset(testset, Group=="E")$Revenue_2011_millions

wilcox.test(revenues.a, revenues.c)
wilcox.test(revenues.a, revenues.b)
wilcox.test(revenues.c, revenues.d)
wilcox.test(revenues.c, revenues.e)


wilcox.test(revenues.c_test, revenues.e_test)
wilcox.test(revenues.c_test, revenues.d_test)
wilcox.test(revenues.d_test, revenues.e_test)

wilcox.test(preint.superfast, preint.fast)
wilcox.test(postint.superfast, postint.fast)
wilcox.test(testset.hot, testset.fast)
