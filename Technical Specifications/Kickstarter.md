## Technical Specification for Kickstarter Model
# Campaign Helper Class
> Variables:
- campaignAddress: address
- goal: uint256
- donations: Hashmap (address -> amountDonated)
> Functions:
- Constructor


# Core Functionality
> Variables:
- campaigns: Hashmap(campaignName -> Campaign)
> Functions:
- donate(campaignName, unint256 amount)
    - takes wolvercoin from the caller's address and donates it to the address of the campaign
    - records the amount donated so that it can be taken out later
    - should check if the goal has been reached
- withdrawDonation(campaingName, uint256 amount)
    - returns wolvercoin from the campaign's address to the caller's address
    - shouldn't be able to withdraw more than they donated
- endCampaign(campaignName)
    - if the campaign's goal was reached, update the website to say that