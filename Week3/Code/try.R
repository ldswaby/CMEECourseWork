doit <- function(x){
  temp_x <- sample(x, replace = TRUE)
  if(length(unique(temp_x)) > 30) {#only take mean if sample was sufficient
    print(paste("Mean of this sample was:", as.character(mean(temp_x))))
  } 
  else {
    stop("Couldn't calculate mean: too few unique values!")
  }
}

popn <- rnorm(50)