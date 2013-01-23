#Tweet Reducer setwd("C:\\Documents and Settings\\Luke\\Desktop\\growth_scout")
# based on http://www.inside-r.org/howto/mining-twitter-airline-consumer-sentiment

library(ggplot2)


#scan list
setwd("C:\\Documents and Settings\\Luke\\Desktop\\bullwhip_effect")
companies <- scan("cloudcomputing.txt",what="",sep="\n")
dbtype <-"_all_tweets.csv"
out_type<-"_scores_histogram.png"

#scan text files for positive and negative words
hu.liu.pos = scan('data/opinion-lexicon-English/positive-words.txt',
                  what='character', comment.char=';')

hu.liu.neg = scan('data/opinion-lexicon-English/negative-words.txt',
             what='character', comment.char=';')

pos.uses <- scan('data/opinion-lexicon-English/pos_use_lexicon.txt',what="",sep="\n")
neg.uses <- scan('data/opinion-lexicon-English/neg_use_lexicon.txt',what="",sep="\n")

pos.values <- scan('data/opinion-lexicon-English/pos_values_lexicon.txt',what="",sep="\n")
neg.values <- scan('data/opinion-lexicon-English/neg_values_lexicon.txt',what="",sep="\n")

pos.choices <- scan('data/opinion-lexicon-English/pos_choices_lexicon.txt',what="",sep="\n")
neg.choices <- scan('data/opinion-lexicon-English/neg_choices_lexicon.txt',what="",sep="\n")

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

N <- length(companies)

summary <- data.frame(company=rep("", N), tweet_volume=rep(NA, N), score_100=rep(NA, N), pop_scale =rep(NA, N), extreme_score =rep(NA,N), uses_score=rep(NA,N), choices_score=rep(NA,N),values_score=rep(NA,N),stringsAsFactors=FALSE) 

for (i in 1:length(companies)) {
    #
    database <- NULL
    tweet_volume <-NULL
    Score.100 <- NULL
    extreme_score <- NULL
    uses_score <-NULL
    choices_score <- NULL
    values_score <- NULL
    
  
    database<- paste(companies[i],dbtype,sep="")
    temp <- try(read.csv(database, sep=',', quote="\'", header=FALSE));
        if(class(temp) == "try-error") next;
    
    #run score on companies data
    temp.scores = score.sentiment(temp$V3, pos.words,
                               neg.words, .progress='text')
    
    #separate extreme scores
    temp.scores$very.pos.bool = temp.scores$score >= 2
    temp.scores$very.neg.bool = temp.scores$score <= -2
    temp.scores$very.pos = as.numeric(temp.scores$very.pos.bool )
    temp.scores$very.neg = as.numeric(temp.scores$very.neg.bool )
    
    #uses, choices, values
    uses = score.sentiment(temp$V3,pos.uses,neg.uses, .progress='text' )
    temp.scores$uses = uses$score
    choices = score.sentiment(temp$V3,pos.choices,neg.choices, .progress='text' )
    temp.scores$choices = choices$score
    values = score.sentiment(temp$V3,pos.values,neg.values, .progress= 'text' )
    temp.scores$values= values$score
    
    temp.scores$uses.score = temp.scores$score * temp.scores$uses
    temp.scores$values.score = temp.scores$score * temp.scores$values
    temp.scores$choices.score = temp.scores$score * temp.scores$choices
    
    uses_score = sum(temp.scores$uses.score)/length(temp.scores$uses.score)
    choices_score = sum(temp.scores$choices.score)/length(temp.scores$choices.score)
    values_score = sum(temp.scores$values.score)/length(temp.scores$values.score)
    
    #calculate extreme scores
    twitter.df = ddply(temp.scores,c('text'), summarise, 
                                        very.pos.count=sum( very.pos ), 
                                        very.neg.count=sum( very.neg ) )
    
    extreme.tot = sum(twitter.df$very.pos.count) + 
      sum(twitter.df$very.neg.count)
    
   extreme_score = round( 100 * sum(twitter.df$very.pos.count) / 
      extreme.tot )
    
    print(companies[i])
    
    #summary statistics
    Score.100 <- mean(temp.scores$score) * 100
    tweet_volume <- length(temp.scores$score)
    pop_scale = tweet_volume * Score.100
    
    print(pop_scale)
    print(tweet_volume)
    print(Score.100)
    print(extreme_score)
    print(uses_score)
    print(choices_score)
    print(values_score)
    
#    create qplot
#     q = qplot(temp.scores$score)
#     q = q + theme_bw()
# 
#     plot.temp <-paste(companies[i],out_type,sep="")
# 
#     ggsave(plot = q,
#       filename = file.path("out", plot.temp),
#       width = 10,
#       height = 10)
    
     
     summary[i, ] <- c(companies[i], tweet_volume, Score.100, pop_scale, extreme_score,uses_score, choices_score, values_score)
}





