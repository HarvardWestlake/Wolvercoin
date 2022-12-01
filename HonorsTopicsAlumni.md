•	Create a depreciateValue method that takes in a String userKey (public key)
	◦	Assert that alumniSet contais userKey
	◦	Assert that the userKey has not made any Wolvercoin transactions in the last year
	◦	Deduce ten percent times the number of inactive months from the value of their Wolvercoin
	▪	Eg. if a user has not made any transactions in one year AFTER BECOMING AN ALUMNI, depreciate their wolvercoin’s value by 10% using the burn method. If a user has not made any transactions in five year AFTER BECOMING AN ALUMNI, depreciate their wolvercoin’s value by 50% using the burn method

## General Specifics
- if you leave your wolvercoin untouched, it depreciates by a percentage

> Variables Needed:
- alumniList: Hashmap (studentAddress -> hasGraduated)


> Functions 
- makeAlumni(address)
    - adds a student to the alumniList Hashmap
    - makes their hasGraduated value True in the map to indicate status

- checkLastTransaction(address)
	- get the student's year
	- subtract that value from current year, call burn on (address, difference)

- burn (address, difference)
	- make a uint256 value for percentage to remove
	- burn that percentage of address' currency




## Upon having the grad or alumni badge -> you get an NFT as proof of completing Honors Topic
- you can either stake your wolvercoin or not
- if you leave your wolvercoin untouched, it depreciates by a percentage