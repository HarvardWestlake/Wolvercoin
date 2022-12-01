# DAO
##### Variables
- float VoterCoinBalance: Money spent on tax and gas will be converted in VoterCoin (VC).
- DAO idea functions off of user submitted contracts that will either be passed or rejected.
- boolean affectsDAO
##### Methods
- boolean hasCoin: 
    - returns true if user has VoterCoin in wallet.
- boolean isStaked: 
    - returns true if user is already staked in a vote with VoterCoin
- void proposeVote: 
   - takes in an entire contract, and a String description for the contract so that users can decide whether or not to stake VoterCoin in this idea. Starts counter for 100 blocks. On 100th block after initial proposal, finishVote is called. If proposed contract directly edits the DAO contract in any way, set affectsDAO to true.
- void finishVote: 
    - if affectsDAO is false, and the majority of VoterCoin currently staked in a vote is staked on a specific side of the vote, and 20% of total VoterCoin is also on that side of the vote, then that side is passed. If a side is passed, call burnCoin. If so side is passed, call returnCoin. If affectsDAO is true, then the proposal must contain 75% of all VoterCoin in existence to be passed.
- void burnCoin: 
    - if the user was on the winning side of the vote, 50% of their VoterCoin is burned, and the other 50% is returned back. This accesses the VoterCoinBalance object.
- void returnCoin: 
    - All VoterCoin is returned to users in full. This accesses the VoterCoinBalance object
- void vote: 
    - takes wallet adress, and amount of VoterCoin staked. The vote method is a form of transaction. All VoterCoin will be sent to the wallet adress of the side of the proposition the user voted for. However, if affectsDAO is true, and the wallet the user is sending VoterCoin from is a top 3 holder of WolverCoin, they will not be allowed to vote. Ingore this extra case if affectsDao is false.
# Single-Year Fail-Safes (Administrator Privilages)
##### Variables
- dynamic array of wallet addresses containing the wallet adresses of selected emergency administrators
##### Methods
- shutDownDAO: 
    - this method shuts down the DAO system in times of emergency. Can only be executed by wallet adress contained in the array of administrator wallets.
##### Notes to Remember
- power of administrator can be altered in an approved proposition with the DAO
- roles of administrators can be divided and specialized with approved propositons
# Multi-Year Fail-Safes (Ensure Only HT Kids Have Access to WolverCoin)
##### Variables
- dynamic array of wallet adresses containign the wallet adresses of current HT students
##### Methods
- ensure there are only HT kids on the network by holding a DAO vote for a contract containing all the wallets of the incoming students. The previous years students will (hopefully) check the list for fraud and trickery, eventually voting for the contract to pass, thus ensuring only HT kids are on network. The proposed contract also removes the previous years HT students from the network, thus ensuring only the new class has access.
    - the contract described above is not a specific method, and will instead be a DAO vote contract specifically designed and proposed each year

