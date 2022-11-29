•	Create a depreciateValue method that takes in a String userKey (public key) 
	◦	Assert that alumniSet contais userKey 
	◦	Assert that the userKey has not made any Wolvercoin transactions in the last month 
	◦	Deduce ten percent times the number of inactive months from the value of their Wolvercoin 
	▪	Eg. if a user has not made any transactions in one month, depreciate their wolvercoin’s value by 10% using the burn method. If a user has not made any transactions in five months, depreciate their wolvercoin’s value by 50% using the burn method