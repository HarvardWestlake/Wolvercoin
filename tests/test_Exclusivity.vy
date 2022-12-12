#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError


exclusivity: Exclusivity=Exclusivity()

@external
def testAddNonTopics():
    exclusivity.addNonTopics(0xC90460533587b81bDC3042329FCf0dB18507b430)#kensuke's public address, just to test
    added: bool=False
    for studentAddress in exclusivity.topicsAddress:
        if studentAddress==0xC90460533587b81bDC3042329FCf0dB18507b430:
            

    
    

