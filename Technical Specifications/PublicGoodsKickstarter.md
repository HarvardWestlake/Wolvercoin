## Structs
- Good
- Donation
## Variables
- goods: HashMap<string, Good>
    - name: string (THIS IS ALSO THE KEY OF THE ENTRY IN THE HASHMAP)
    - goal: the donation goal to be met
    - donations: Donation[]
    - totalDonations: the total amount of money donated so far
## Methods
- createGood(String nameOfGood, int price)
    - makes a good with whatever price is decided and is not redeemed until curent is equal to price.
        - An entry is created in the Goods hashmap, with the key as the name of the good
        - Reject if there is already a good with the same name
    - puts it on whatever website Mr. Theiss makes so people can buy
- contribute(String nameOfGood, int amount)
    - people can contribute to a public good of id _id_ with amount _amount_ until the price is met
    - Adds _amount_ to the user's _donations_ entry
    - Increments totalDonations
    - Rejects if the goal is already met
    - Caps donation at the amount needed to achieve the goal
- retract(String nameOfGood, uint256 adress)
    - Removes _amount_ from the user's _donations_ entry
    - Make sure user can't retract money that haven't put in, i.e. _amount_ <= donations[user]
    - decrements totalDonations
- complete(String nameOfGood)
    - If the goal is met, the good is redeemed, and the good is deleted from the database
    - if the goal is not met, all donators are refunded their total donation amount
    - This function can be called at any time by the creator of the public good
