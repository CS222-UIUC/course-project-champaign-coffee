# Algorithm 

Our algorithm will prompt the user for an input for 6 different multiple choice questions. Each question answer will have a value from 1 to 20 (doubles may be used), 
and the algorithm will compute an average of these values. We will preemptively have the corresponding data values calculated for each individual coffee entry in the 
corresponding restaurants, and in turn the average value of each entry for each corresponding restaurant. It will then match the average of the user selected responses 
with the shop that is closest to it in premeptively calculated value, and in turn will reccomend the drink that has the least total difference in value with the user 
selected responses for each of the assigned categories (results of the questions). 

# Questions
1. Will ask what type of coffee drink (espresso, cappucino, frappucini, macchiatto, etc).
2. Will ask the desired price range. Point value here will be based on an even split between the minimum and maximum price of coffee. 
3. Will ask any flavor preference (none, chocolate, ice cream, etc).
4. Will ask location preference 
5. Will ask preferred ratings and how much they matter
6. How much its proximity to various campus buildings/departments matters.

3/22 Notes

Will filter possibilities after each question that asks discrete values, while for continous like price or flavor (which can be interpreted on a scale based on type), these will be pre computed and the algo will attempt to minimize the differences.

Location (two parameters: desired proximity to what and how much it matters to user on a scale)

Can return both results for that and closest on campus if user selects that that matters.

Can get location from ip.
