#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: variables.sh
# Desc: Playing around with variables
# Arguments: NA
# Date: Oct 2020

# Shows use of variables
MyVar='My String'
echo "The variable is currently named '$MyVar'"
echo 'Please enter a new string'
read MyVar
echo "The variable is currently named '$MyVar'"

# Managing multiple variables
echo 'Enter 2 numbers separates by a space(s)'
read a b
echo 'You entered' $a 'and' $b'. Their sum is:'
mysum=$(expr $a + $b)
echo $mysum