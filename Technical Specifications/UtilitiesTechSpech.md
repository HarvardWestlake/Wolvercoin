*Created by Aariz, Wyatt, and Zach*

### Spend 30 wolvercoin you can place an image on the wolverscreens
- `buyWolverscreen` function
    - parameters: `imageURL`, ensure that image is 1280x720 pixels
    - verify that user has over 30 wolvercoin, and subtract that from their wallet
    - send a POST request to Node server (or other web server) that sends email to `jchurch@hw.com` from `cstopics@hw.com`
        - email subject: "New Wolverscreen image"
        - email content: `imageURL` parameter
        - note that Mr. Church will need to approve image to make sure it's appropriate before adding it

#### Wolvercoin in the bookstore
> Anyone can create an NFTs that represents a physical products they own
> - Problem: Validating that the person who created the NFT has the product
>
> The NFT is sold through and action (see DutchActions.md)
>
> The NFT can be burnt by its owner to get the person who created it to send you the item
> - Problem: There is no way to garentee that upon burning it the person will send it to you.
> - Solution: Seller clout. If you trust the person who is sending it to you (based on previous good transactions) then you can likely trust them.

### Can spend wolvercoin for direct grade
- Spend Wolvercoin for Direct Grade
    - Problem
        - Difficulty integrating with the hub
    - Solution
        - Create as an Auction Item for different assignments
        - *Refer to Auction Psuedo Code for creating auction items*


*Refer to design specs for more information on each feature*