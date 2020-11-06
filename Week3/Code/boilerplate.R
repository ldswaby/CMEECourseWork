##############################
### A boilerplate R script ###
##############################

MyFunction <- function(Arg1, Arg2){

    print(paste("Argument", as.character(Arg1), "is type", class(Arg1)))
    print(paste("Argument", as.character(Arg2), "is type", class(Arg2)))

    return (c(Arg1, Arg2))
}

MyFunction(1, 2)
MyFunction(1, "two")
MyFunction("Riki", "Tiki")