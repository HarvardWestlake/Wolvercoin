Variables:

    stakeAmounts --> HashMap that records the users that have staked and how much they've staked; keys are user addresses, values are amounts staked by users

    stakeDates --> HashMap that records the users that have staked and the date that they staked; keys are user addresses, values are dates the users staked

    bank --> the bank's wallet address

    totalOfTransactions unit256 
        variable that keeps track of the total Wolvercoin being transcated through the class

Methods:

    constructor
        set bank to msg.sender

    stake(address userAddress, uint256 amountStaked)
        - userAddress is the address of the wallet trying to stake
        - amountStaked is input by user
        - sends amountStaked to the wallet of the bank
        - stakeAmounts.put(userAddress, amountStaked)
        uint256 date --> get current date and time
        - stakeDates.put(userAddress, date)

    unstake(address userAddress)
        if date staked that was recorded for this user in stakeDates is greater than 2 weeks ago from today:
            - uint256 amountUnstaked --> 2/3 of initial amount staked by user
            - burn the other 1/3
        else:
            - uint256 amountUnstaked --> calculate the percent change between transactions today vs yesterday and multiply (1 + that change) against the initial amount staked by the userAddress
        - send amountUnstaked to userAddress
        - remove key mapping for userAddress from stakeAmounts HashMap
        - remove key mapping for userAddress from stakeDates HashMap
    
    take10Percent
        takes 10% off of totalOfTransactions variable 
        diminishes totalOfTransactions by 10% because that 10% will be put into liquidity provider
        returns a unit256 value that is that 10% of totalOfTransactions
    
    depost10Percent
        deposits that 10% into a liquidity provider (uniswap, sushiswap, other internet liquitiy provider)
        returns true if the deposit is successful, false otherwise  

