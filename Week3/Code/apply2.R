# Create 10x10 matrix of normally distributed numbers
# and multiply each element by 100 

SomeOperation <- function(v){
    # if sum of input vector's elements is positive, 
    # multiply vec by 100
    if (sum(v) > 0){
        return (v * 100)
    }
    return (v)
}

M <- matrix(rnorm(100), 10, 10)
print(apply(M, 1, SomeOperation))