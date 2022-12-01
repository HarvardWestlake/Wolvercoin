Kickstarter model tech spec:

Variables
  >price - uint256
  
  >pool - address
  
  >donators - hashmap[address, uint256]
  
Methods
  >constructor
  >>sets the target price and pool address
 
 >donate(uint256 amount)->bool
  >>transacts amount from donator's wallet and adds it to the contribution wallet
  >>checks if the contribution wallet's account has reached the goal price if it has then the wolvercoin either gets sent to the seller or burned
  >>adds the donator's address and their donation amount to the donators variable
  
  >remove(uint256 amount)->bool
  >>checks the address on donators list, if the address asking to remove has donated <=amount, then transfer amount from the pool address - returns true
  >>checks if the price has been reached, if it has then don't allow anyone to remove - returns false
  
  
  
