# Unorganized NFTs/Gamify (General)
1. Mint NFTs (Wolverines which can breed)
  - Have traits
  - see below for more specific design
2. be able to create NFTs and upload to the wolvercoin network
  - upload NFTs and pay for them with Wolvercoin**
  - tax creators to prevent too much nft actions (creation, but, sell, trade)
    - aka any transaction with the NFT costs some amount of gas fees
3. Weekly NFT competitions (see below for details)

***

# Design (Specific)
1. Create a 3rd Coin:
  - For user-created items
  - For each NFT a user mints, they get a small amount of GAME coin when their NFT is purchased by another user which equals a percentage of the NFT’s value
  - GAME coin can be used to artificially increase an NFT’s value when it is created
2. Wolverine NFTs
    - Each Wolverine has unique, randomly-generated traits (i.e. Mouth shape, hats, etc) that appear after it is minted
        - Traits have varying rarity
        - ![changing traits](https://queue-it.com/media/ss1dxknh/bored-apes.jpg)
    - Can "breed" Wolverines
        - must have 2 Wolverines to breed
            - Breeding generates a Wolverine "Pup" which have a specific powers/values
                - The better the power, the lower the chances of getting this pup
                - Pups can be used to compete in competitions/mini games (costs some GAME coin to compete)
                    - If a Pup loses, burn it
                    - If a Pup wins, address gets GAME/some other prize
        - Breeding costs a gas fee and must wait a 2 days before a Wolverine can breed again
    - Wolverines can be minted, bought and sold on GAME network as well
    - Every week a wolverine NFT(with unique traits) is minted and a random user is chosen to recieve it
        - The more you intereacted with Wolvercoin that week increases your chance at recieving the NFT

