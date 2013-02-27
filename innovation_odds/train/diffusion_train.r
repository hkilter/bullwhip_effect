
#set the working directory
setwd('C:\\Documents and Settings\\Luke\\Desktop\\green_banana_citations\\train')

#load in the training data
tech_train <- read.csv("diffusion_revenue_time.csv",header =TRUE)

#run rpart model

tech_train.model <- rpart(reached_500_million~Timeto50m+Timeof50m+Industry+category+X2nd_category+Available.years+percent_time_used, data=tech_train)

#display tree
tech_train.model

#plotting information
plot(tech_train.model, uniform=TRUE, compress=TRUE, lty=3, branch=0.7)
text(tech_train.model, all=TRUE,digits=7, use.n=TRUE, cex=0.8, xpd=TRUE)

#model error: needs test set to compare with
calculate_rms_error()