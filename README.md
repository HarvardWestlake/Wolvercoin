# Wolvercoin

Wolvercoin (WvC) is an ERC20 with various functionality including ________. It is designed for public use while also including additional functionality for students from Harvard Westlake High School. The contract can be conviently interacted with at (insert front end address).

# Issues
If you find anything wrong you can submit it on the [issues page](https://github.com/HarvardWestlake/Wolvercoin/issues) alternativly you can open a pull request with the fix explaining the problem.

# Documentation

## Rembursment 

text and words and stuff


## Voting

**proposeVote(contract: address, explaination: String[255])**: Takes an address that is either a contract or person and opens a vote with a specified explaination for its purpose setting the end of the vote to the current vote duration. The method can also be paid money which will be stored until the end of the vote where it can either be sent to address or returned.

> ### Submitting a contract
> Submitting a contract is a very versitile request as what it will do is one the vote sucsess grant the contract adminstator permision, send the stored money then run the meathod named (INSERT NAME). This is primarily ment to be used to run setters with adminstator status. This can allow things such as ellections, system changes and much more.
>
> This is mean to make proposals you need to write some code but don't panic yet as you can use [interfaces](https://vyper.readthedocs.io/en/stable/interfaces.html) to make this coding much more simple. Sample interfaces for many actions you may want to do can be found [here](https://youtu.be/dQw4w9WgXcQ).

> ### Submitting an address
> This has much less use as all it will do is store money and give it to the address on a sucsessful vote. Is mainly meant to be called from communal reference to allow transfers of money (say to a charity) to be voted on

