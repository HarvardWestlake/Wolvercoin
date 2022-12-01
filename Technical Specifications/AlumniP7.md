NFT Badge Function

- Create a HashSet of student objects student object that each have an ID (public key) and graduating year (integer). Create a hashSet (alumniSet) that stores a student object of every Honors Topic graduate/alum
- Create an addAlumni method with no parameters
	- Iterate through lists of student objects and if the current year is greater than the student's graduating year, remove that student from the student set and add it to the alumni list
		- Call mintNFT method and assign it to the student moved to alumni set
- Add a parameter to the stake method that takes in a String userKey (public key)
	- Add an assertion statement to the stake method
		- assert that alumniSet contains userName, allowing them to proceed and stake their Wolvercoin
		- If HashSet does not contain userName, subsequent code will not run

	
**This would mean only alumni can stake Wolvercoin. Is that what you want?**

- **We might have to create a yearly fee system.**

## Alternate Depreciate Method if Last Transaction doesn't work
- Two arrays. 1 = allAlumni 2 = nonActiveAlumni
- We would also need a method that only alumni can run that removes them from the nonActiveAlumni list by paying a fee

- Create a depreciateValue method that takes in a dynamic array of alumni userKeys that have not paid the yearly fee (public key): nonActiveAlumni
	- This method should run on the first day of every month
	- It should loop through all alumni's userKeys
	- Deduce ten percent times the number of inactive months from the value of their Wolvercoin
	- Eg. if a user is an alumni, depreciate their wolvercoin’s value by 10% using the burn method. If a user has not made any transactions in five months, depreciate their wolvercoin’s value by 50% using the burn method
