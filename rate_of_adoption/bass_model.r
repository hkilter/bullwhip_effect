# BASS Diffusion Model

# three parameters:
# the total number of people who eventually buy the product, m;
# the coefficient of innovation, p;
# and the coefficient of imitation, q

# example

#time variables
#known times
T79 <- 1:10
#project 10 years time
Tdelt <- (1:100) / 10

#sequence of adoption
Sales <- c(840,1470,2110,4000, 7590, 10950, 10530, 9470, 7790, 5890)
Cusales <- cumsum(Sales)

#Non-linear least squares. For when you know the form of a model. 
Bass.nls <- nls(Sales ~ M * ( ((P+Q)^2 / P) * exp(-(P+Q) * T79) ) /(1+(Q/P)*exp(-(P+Q)*T79))^2,
                start = list(M=60630, P=0.03, Q=0.38))

summary(Bass.nls)

#get coefficient
Bcoef <- coef(Bass.nls)

m <- Bcoef[1]
p <- Bcoef[2]
q <- Bcoef[3]

# setting the starting value for M to the recorded total sales.
ngete <- exp(-(p+q) * Tdelt)

# plot probability density function
Bpdf <- m * ( (p+q)^2 / p ) * ngete / (1 + (q/p) * ngete)^2
plot(Tdelt, Bpdf, xlab = "Year from 1979",ylab = "Sales per year", type='l')

#actual sales
points(T79, Sales)

# continuous density function
Bcdf <- m * (1 - ngete)/(1 + (q/p)*ngete)
plot(Tdelt, Bcdf, xlab = "Years", ylab = "Cumulative Adoption", type='l')
points(T79, Cusales)

#when q=0, only Innovator without immitators.
Ipdf<- m * ( (p+0)^2 / p ) * exp(-(p+0) * Tdelt) / (1 + (0/p) * exp(-(p+0) * Tdelt))^2
plot(Tdelt, Ipdf, xlab = "Year from 1979",ylab = "Isales per year", type='l')
Impdf<-Bpdf-Ipdf
plot(Tdelt, Bpdf, xlab = "Year from 1979",ylab = "Sales per year", type='l', col="red")
lines(Tdelt,Impdf,col="green")
lines(Tdelt,Ipdf,col="blue")

# when q=0, only Innovator without immitators.
Icdf<-m * (1 - exp(-(p+0) * Tdelt))/(1 + (0/p)*exp(-(p+0) * Tdelt))
plot(Tdelt, Icdf, xlab = "Year from 1979",ylab = "ICumulative sales", type='l')
Imcdf<-m * (1 - ngete)/(1 + (q/p)*ngete)-Icdf
plot(Tdelt, Imcdf, xlab = "Year from 1979",ylab = "Cumulative sales", type='l', col="red")
lines(Tdelt,Bcdf,col="green")
lines(Tdelt,Icdf,col="blue")
