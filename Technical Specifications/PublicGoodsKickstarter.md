
## Variables
- goods[]
    - goal: the donation goal to be met
    - donations{user, amount}: the amount of money each user has donated
## Methods
- createGood(String nameOfGood, int price)
    - makes a good with whatever price is decided and is not redeemed until curent is equal to price.
    - puts it on whatever website Mr. Theiss makes so people can buy
    - returns the ID of the good for future use
- contribute(int id, int amount)
    - people can contribute to a public good of id _id_ with amount _amount_ until the price is met
    - Adds _amount_ to the user's _donations_ entry
- retract(String nameOfGood, uint256 adress)
    - Removes _amount_ from the user's _donations_ entry
    - Make sure user can't retract money that haven't put in, i.e. _amount_ <= donations[user]
- complete()
    - If the goal is met, the good is redeemed, and the good is deleted from the database
    - if the goal is not met, all donators are refunded their total donation amount
    - This function can be called at any time by the creator of the public good