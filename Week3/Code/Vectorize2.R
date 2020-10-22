# Runs the stochastic Ricker equation with gaussian fluctuations

rm(list=ls()) #??

stochrick<-function(p0=runif(1000,.5,1.5),r=1.2,K=1,sigma=0.2,numyears=100)
{
  #initialize 
  N<-matrix(NA,numyears,length(p0)) #100x1000 matrix by default (yearsxpop)
  N[1,]<-p0
  
  for (pop in 1:length(p0)){#loop through the populations (cols)
    
    for (yr in 2:numyears){ #for each pop, loop through the years (rows)

      N[yr,pop] <- N[yr-1,pop] * exp(r * (1 - N[yr - 1,pop] / K) + rnorm(1,0,sigma))
    
    }
  
  }
 return(N)

}

# Now write another function called stochrickvect that vectorizes the above 
# to the extent possible, with improved performance: 

stochrickvect <- function(p0=runif(1000,.5,1.5),r=1.2,K=1,sigma=0.2,numyears=100)
{
  #initialize 
  N <- matrix(NA,numyears,length(p0)) #DEFAULT: 100x1000 matrix of NAs (yearsxpop)
  N[1,] <- p0 #DEFAULT: row 1 = year 1 = 1000 random numbers between 0.5 and 1.5
  
  for (yr in 2:numyears){# loop through the years (rows)
    
    N[yr,] <- N[yr-1,] * exp(r * (1 - N[yr-1,] / K) + rnorm(1,0,sigma))
  
    } 
    
  return(N)
}

print("Non-vectorized Stochastic Ricker takes:")
print(system.time(res2<-stochrick()))
print("Vectorized Stochastic Ricker takes:")
print(system.time(res2<-stochrickvect()))
