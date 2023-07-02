# shuffler
A simple program that shuffles a string and shuffles them again in multiple threads till the original string is obtained. A simultation for probability of obtaining the same combination after shuffling. 

Program to experimentally calculate the probability of shuffling a string until the same string is obtained.

Probability of shuffling a string without repetition is 1/(n!)

-----Probability of shuffling a string by m threads at the same time-----

A = Atleast one success

                          P(A) = 1-((n!-1)**m/(n!)**m)
where m is the number of threads and n is the number of letters (without repetition)
