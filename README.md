# Wolvercoin

Wolvercoin (WvC) is an ERC20 with various functionality including ________. It is designed for public use while also including additional functionality for students from Harvard Westlake High School. The contract can be conviently interacted with at (insert front end address).

# Issues
If you find anything wrong you can submit it on the [issues page](https://github.com/HarvardWestlake/Wolvercoin/issues) alternativly you can open a pull request with the fix explaining the problem.

# Application Details
Application is a standard react app created with `npx create-react-app app`
Utils for web3 are provided by `npm install @web3uikit/core @web3uikit/web3 @web3uikit/icons`


# Setting up
Wolvercoin consists of two parts, the Web UI and the Ethereum Contracts

## Web UI
To test the Web UI, inside the ./Wolvercoin/app/ directory type `npm start`.  If you get any error regarding a package not being found, please install all packages by typing `npm install` and then trying to start npm again.

## Ethereum Contracts
To test Etheruem contracts inside the ./Wolvercoin/ directory type `brownie test`
