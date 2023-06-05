# Deployment

## Sign up for Alchemy
1. We will be using Alchemy to deploy our contract. [You can also use Infura, etc.](https://eth-brownie.readthedocs.io/en/stable/network-management.html#using-infura)
2. Sign up for an Alchemy account: alchemy.com
3. Create an Alchemy app on the Goerli testnet.
4. Click "View key", copy the portion after the last slash under "HTTPS". This is your Alchemy Project ID.
5. Paste the following into a file called `.env` and paste your project ID:
```
WEB3_ALCHEMY_PROJECT_ID=123_my_project_id_456
```
6. Run:
```bash
brownie networks set_provider alchemy
```


## Add your account to Brownie

1.
```bash
brownie accounts new my_account
```
2. Go to MetaMask --> 3 dots --> Export Private Key --> Copy the private key and paste it in the terminal
3. Enter a password to encrypt your account

## Deploy the contract

1. 
```bash
brownie run deploy --network goerli
```
2. Enter your account password
3. Copy-paste the addresses printed out at the end to the file `app/src/components/Contexts/config.js`