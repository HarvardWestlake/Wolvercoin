## Utilities 

### Spend 30 wolvercoin you can place an image on the wolverscreens
- `buyWolverscreen` function
    - parameters: `imageURL`, ensure that image is 1280x720 pixels
    - verify that user has over 30 wolvercoin, and subtract that from their wallet
    - send a POST request to Node server (or other web server) that sends email to `jchurch@hw.com` from `cstopics@hw.com`
        - email subject: "New Wolverscreen image"
        - email content: `imageURL` parameter
        - note that Mr. Church will need to approve image to make sure it's appropriate before adding it

#### Wolvercoin in the bookstore
> USES SAME FUNCTIONALITY AS ACTIONS BUT MORE
>
> Variables
> - boundNFTs - `hashMap(productSha uint256, productOwner address)`
>   - uint256 is the address of the NFT
>   - address is the person who created it
>
> Methods
> - `createBoundNFT(uint256 productSha)` - product sha is sha of photo containing item. Creates an NFTs that represents a physical products (see problem 1)
> - `redeemProduct(uint256 productSha)` - finds the owner and informs them to send the item to the person who called method (see problem 2)
> 
> Problems
> 1) There is no way to garrentee that upon burning it the person will send it to you.
> 2) Validating that the person who created the NFT has the product
> 
> Solutions
> 2) Seller clout. If you trust the person who is sending it to you (based on previous good transactions) then you can likely trust them.

### Can spend wolvercoin for direct grade
- Spend Wolvercoin for Direct Grade   
    - Create as an Auction Item for different assignments - just like any other NFT
        - Copy other NFT class 
        - Each Grade NFT can be initialized with number of points bought and the assignment it goes to
        - Actual NFT's created and moderated by Mr. Theiss so no further automation is needed.