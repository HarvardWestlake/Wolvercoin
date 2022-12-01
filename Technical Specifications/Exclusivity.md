	1.	Variables:  
      ->topicsAddress : Array of honors topics students’ wallet addresses 
	2.	Methods: 
      ->addNonTopics (parameter: address of contender to be added as topics student) 
            ->Look at voting method from function 1 (audrey’s function about voting) 
                  ->Use address from voting method and see current balance  
	          ->If current balance divided by number of addresses in topicsAddress = 1, then student can be added into topicsAddress array 
	    ->removeTopics (parameter: address of contender to be removed as topics student) 
	    	    ->Look at voting method from function 1 (audrey’s function about voting) 
		    	       ->Use address from voting method and see current balance  
		    	  ->If current balance divided by number of addresses in topicsAddress = 1, then student is removed from topicsAddress array 
