#Tweet Reducer setwd("C:\\Documents and Settings\\Luke\\Desktop\\growth_scout")
# based on http://www.inside-r.org/howto/mining-twitter-airline-consumer-sentiment

library(twitteR)
library(ggplot2)

#scan list
setwd("C:\\Documents and Settings\\Luke\\Desktop\\growth_scout")
companies <- scan("growthscout_test.txt",what="",sep="\n")
dbtype <- "tweets_search_timeline_artshub.csv"

# for later /data.path <- file.path("out")

database<-paste(companies[1],dbtype,sep="")

#temp <- read.csv(database, sep=',', quote="\'", header=FALSE)
temp<- read.csv("tweets_search_timeline_artshub_tweet.csv", sep=',',quote="\'",header=FALSE)
#square <- read.csv('square_comparative_tweets.csv', sep=',',quote="\'",header=FALSE)

#write to connect to couchdb
#stripe.comps <- fromJSON(getURL("http://localhost:5984/tweets_search_timeline_stripe/_design/tweet/_view/comparative_tweet"))

#Search for tweets with R pacakge
#delta.tweets = searchTwitter('@delta', n=1500)
#verify
#length(delta.tweets)
#tweet = delta.tweets[[1]]

#scan text files for positive and negative words
hu.liu.pos = scan('data/opinion-lexicon-English/positive-words.txt',
                  what='character', comment.char=';')

hu.liu.neg = scan('data/opinion-lexicon-English/negative-words.txt',
             what='character', comment.char=';')

pos.words = c(hu.liu.pos, 'upgrade')

neg.words = c(hu.liu.neg, 'wtf', 'wait', 'waiting', 'epicfail', 'mechanical')

# Sentiment Scoring

score.sentiment = function(sentences, pos.words, neg.words, .progress='none')
{
  require(plyr)
  require(stringr)
  
  # we got a vector of sentences. plyr will handle a list
  # or a vector as an "l" for us
  # we want a simple array of scores back, so we use 
  # "l" + "a" + "ply" = "laply":
  scores = laply(sentences, function(sentence, pos.words, neg.words) {
    
    # clean up sentences with R's regex-driven global substitute, gsub():
    sentence = gsub('[[:punct:]]', '', sentence)
    sentence = gsub('[[:cntrl:]]', '', sentence)
    sentence = gsub('\\d+', '', sentence)
    # and convert to lower case:
    sentence = tolower(sentence)
    
    # split into words. str_split is in the stringr package
    word.list = str_split(sentence, '\\s+')
    # sometimes a list() is one level of hierarchy too much
    words = unlist(word.list)
    
    # compare our words to the dictionaries of positive & negative terms
    pos.matches = match(words, pos.words)
    neg.matches = match(words, neg.words)
    
    # match() returns the position of the matched term or NA
    # we just want a TRUE/FALSE:
    pos.matches = !is.na(pos.matches)
    neg.matches = !is.na(neg.matches)
    
    # and conveniently enough, TRUE/FALSE will be treated as 1/0 by sum():
    score = sum(pos.matches) - sum(neg.matches)
    
    return(score)
  }, pos.words, neg.words, .progress=.progress )
  
  scores.df = data.frame(score=scores, text=sentences)
  return(scores.df)
}

#test sentences
#sample = c("You're awesome and I love you", 
#           "I hate and hate and hate. So angry. Die!", 
#           "Impressed and amazed: you are peerless in your 
#  				achievement of unparalleled mediocrity.")

# run code on test
#result = score.sentiment(sample, pos.words, neg.words)

#result[,'score']

#run on delta data
temp.scores = score.sentiment(temp$V2, pos.words,
                               neg.words, .progress='text')

#create new column in a data frame
#delta.scores$airline = 'Delta'
#delta.scores$code = 'DL’

#create histogram
#hist(delta.scores$score)
hist(temp.scores$score)

#create qplot
q = qplot(temp.scores$score)
q = q + theme_bw()
q

sum(temp.scores$score)/length(temp.scores$score)
#end loop- next file

#capture all the scores from a sector
#all.scores = rbind( american.scores, delta.scores, jetblue.scores,
#  					southwest.scores, united.scores, us.scores )

#compare sector distribution
#g = ggplot(data=all.scores, mapping=aes(x=score, fill=airline) )
#g = g + geom_bar(binwidth=1)
#g = g + facet_grid(airline~.)

#g = g + theme_bw() + scale_fill_brewer()

#focus on very negative and postive
#all.scores$very.pos.bool = all.scores$score >= 2
#all.scores$very.neg.bool = all.scores$score <= -2
#all.scores[c(1,6,47,99), c(1, 3:8)]

#twitter.df = ddply(all.scores, c('airline', 'code'), summarise, 
#                    very.pos.count=sum( very.pos ), 
#                     very.neg.count=sum( very.neg ) )

# twitter.df$very.tot = twitter.df$very.pos.count + 
#                        twitter.df$very.neg.count

# twitter.df$score = round( 100 * twitter.df$very.pos.count / 
#                                  twitter.df$very.tot )

#orderBy(~-score, twitter.df)
