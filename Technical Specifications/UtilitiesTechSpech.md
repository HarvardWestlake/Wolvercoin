*Created by Aariz, Wyatt, and Zach*

### Spend 30 wolvercoin you can place an image on the wolverscreens
- `buyWolverscreen` function
    - parameters: `imageURL`, ensure that image is 1280x720 pixels
    - verify that user has over 30 wolvercoin, and subtract that from their wallet
    - send a POST request to Node server (or other web server) that sends email to `jchurch@hw.com` from `cstopics@hw.com`
        - email subject: "New Wolverscreen image"
        - email content: `imageURL` parameter
        - note that Mr. Church will need to approve image to make sure it's appropriate before adding it

### Wolvercoin could be used in the bookstore, hoco/prom tickets, and HW events, caf
- Create a Harvard Westlake Administration Wallet
    - This wallet would be owned by the school
    - In order for students to spend wolvercoin at cafeteria:
        - Students would sent wolvercoin to the HW wallet address
        - HW Staff would check to see if transaction went through to the HW address for confirmation of purchase
- Refer to Gas-Free Distribution file for gas fees

### Can spend wolvercoin for direct grade
- Spend Wolvercoin for Direct Grade   
    - Create as an Auction Item for different assignments - just like any other NFT
        - Copy other NFT class 
        - Each Grade NFT can be initialized with number of points bought and the assignment it goes to
        - Actual NFT's created and moderated by Mr. Theiss so no further automation is needed.