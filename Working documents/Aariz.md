Spend 30 wolvercoin you can place an image on the wolverscreens
1. Only available to Honors Topics students
2. Every 10 extra wolvercoin added to the pot, the photo stays on the screen for one minute more

- `buyWolverscreen` function
    - parameters: `imageURL`, ensure that image is 1280x720 pixels
    - verify that user has over 30 wolvercoin, and subtract that from their wallet
    - send a POST request to Node server (or other web server) that sends email to `jchurch@hw.com` from `cstopics@hw.com`
        - email subject: "New Wolverscreen image"
        - email content: `imageURL` parameter
        - note that Mr. Church will need to approve image to make sure it's appropriate before adding it