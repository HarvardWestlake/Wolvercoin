
## Alumni Tag

- Create a HashSet (alumniSet) that stores the names (public key) of every Honors Topic graduate/alum

- Create an addAlumni method with no parameters

- If a Wolvercoin user is an alum, add to alumniSet and mint them an NFT by calling NFT method

- Add a parameter to the stake method that takes in a String userKey (public key)

- Add an assertion statement to the stake method

- assert that alumniSet contains userName, allowing them to proceed and stake their Wolvercoin

- If HashSet does not contain userName, subsequent code will not run

**This would mean only alumni can stake Wolvercoin. Is that what you want?**



## Alternate Depreciate Method if Last Transaction doesn't work
**We might have to create a yearly fee system.**

- Two arrays: 1 = allAlumni 2 = nonActiveAlumni

- We would also need a method that only alumni can run that removes them from the nonActiveAlumni list by paying a fee called remainActive()

  

- Create a depreciateValue method that takes in an array (nonActiveAlumni) of alumni userKeys that have not paid the yearly fee (public key): 

- This method should run on the first day of every month

- It should loop through all alumni's userKeys

- Deduce ten percent from the value of their Wolvercoin

- Eg. if a user is an alumni, and they have paid to remove themselves from inactiveAlumni depreciate their wolvercoin’s value by 0% using the burn method. If a user has not done so, reduce the wolvercoin in their wallet by 10%