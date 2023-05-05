# Algorithm 

Our algorithm will prompt the user for an input for 3 different multiple choice and one numeric input question. The response to two of the questions will allow us to rank the user's preference for proximity to campus and the rating of a coffee shop on a scale from 0 to 2 inclusive. Then, our algorithm will take in that data, in addition to the answer to the first question, the desired coffee type, and ultimately the price range the user selects, and will reccomend a coffee drink based on the following criteria: It will select the drink that matches the coffee type and price range with the lowest price, it will also select a drink that matches that criteria but with the constraint that the rating is 4 or 5, along with another drink with the same criteria but with th constraint instead being that it's proximate to campus (proximity of 1). If the user ranked proximity importance as greater than rating importance, we return the drink with that constraint, while if rating importance was ranked greater than we return the drink with that constraint instead. Otherwise rating and proximity importance must be equal, so if they are ranked higher than 0 we simply return the drink between the two with the lowest price, and if they are both 0 then we simply return the generic drink with the lowest price. This algorithm will therefore always be factoring in the user preference, while emphasizing lower prices in the result it returns. 



# Questions
1. Will ask what type of coffee drink (espresso, cappucino, frappe, macchiatto, etc).
2. Will ask the desired price range, namely the min and max price. 
3. Will ask how much proximity data matters.
4. Will ask how much ratings of the coffee shop matters.



