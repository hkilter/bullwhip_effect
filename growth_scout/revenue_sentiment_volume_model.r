#Models of influence of money on gains


company <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\growth_scout\\simple_score1.csv", header=TRUE)
#disruptive_range <- read.csv("C:\\Documents and Settings\\Luke\\Desktop\\Programming\\disruptive_range.csv", header=TRUE)

#linear models

funding_rounds.lm <- lm(funding_rounds~ tweet_volume+ score_100, data=company)

disruptive_range.lm <- lm(gain~ funding, data=disruptive_range)

cloud_revenue.lm <- lm(revenue~ tweet_volume+uses_score+ choices_score+values_score, data=company)

#graphs
p <- ggplot(disruptive_range, aes(x =funding,y=gain))
p + geom_point()
r <- ggplot(disruptive, aes(x =funding,y=gain))
r + geom_point()