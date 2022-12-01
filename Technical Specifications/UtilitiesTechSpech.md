*Created by Aariz, Wyatt, and Zach*

### Spend 30 wolvercoin you can place an image on the wolverscreens

##### Variables
- `String[100] imageURL` - url to image that should be added to wolverscreen
- `address user` - address of user who wants to buy wolverscreen 

##### Constructors
- sets `imageURL` and `user` variables

##### Methods
- `buyWolverscreen` function
    - ensure that image is 1280x720 pixels
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
    - Problem
        - Difficulty integrating with the hub
    - Solution
        - Create as an Auction Item for different assignments
        - *Refer to Auction Psuedo Code for creating auction items*


*Refer to design specs for more information on each feature*