#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError

@external
def testVote():
    exclusivity: Exclusivity=Exclusivity()
    exclusivity.classSize = 100
    exclusivity.topicsAddress.append(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    exclusivity.vote(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    valueChanged: bool=False
        if balance(0xf34b09E22f5115af490eeb7460304aB80c90399E)>=1:
            valueChanged = True
    assert valueChanged
    valueChanged = false
    
    exclusivity.admin[0xf34b09E22f5115af490eeb7460304aB80c90399E] = True
    exclusivity.vote(0xf34b09E22f5115af490eeb7460304aB80c90399E)
     if balance(0xf34b09E22f5115af490eeb7460304aB80c90399E)>=16:
            valueChanged = True
    assert valueChanged
    
@external
def testTally():
    exclusivity: Exclusivity=Exclusivity()
    exclusivity.percentage = 0.51
    exclusivity.tallyVotes(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    
    removed: bool=True
    for studentAddress in exclusivity.topicsAddress:
        if studentAddress==0xf34b09E22f5115af490eeb7460304aB80c90399E:
            removed = False
            break
    
    assert removed
    
@external
def testAddNonTopics():
    exclusivity: Exclusivity=Exclusivity()
    exclusivity.percentage=1
    exclusivity.addNonTopics(0xC90460533587b81bDC3042329FCf0dB18507b430)#kensuke's public address, just to test
    added: bool=False
    for studentAddress in exclusivity.topicsAddress:
        if studentAddress==0xC90460533587b81bDC3042329FCf0dB18507b430:
            added=True
            break
    assert added,"should add if percentage is 1 or greater"

    exclusivity.topicsAddress.pop()
    exclusivity.percentage=0.2
    exclusivity.addNonTopics(0xC90460533587b81bDC3042329FCf0dB18507b430)
    added=False
    for studentAddress in exclusivity.topicsAddress:
        if studentAddress==0xC90460533587b81bDC3042329FCf0dB18507b430:
            added=True
            break 
    assert not added,"should not add if percentage is lower than 1"
    


def testRemoveTopics():
    exclusivity: Exclusivity=Exclusivity()
    exclusivity.topicsAddress.append(0xC90460533587b81bDC3042329FCf0dB18507b430
    exclusivity.percentage=1
    exclusivity.removeNonTopics(0xC90460533587b81bDC3042329FCf0dB18507b430)
    removed: bool=True
    for studentAddress in exclusivity.topicsAddress:
        if studentAddress==0xC90460533587b81bDC3042329FCf0dB18507b430:
            removed=False
            break
    assert removed, "should remove if percentage is greater than or equal to 1"

    exclusivity.topicsAddress.append(0xC90460533587b81bDC3042329FCf0dB18507b430
    exclusivity.percentage=0.2
    exclusivity.removeNonTopics(0xC90460533587b81bDC3042329FCf0dB18507b430)
    removed=True
    for studentAddress in exclusivity.topicsAddress:
        if studentAddress==0xC90460533587b81bDC3042329FCf0dB18507b430:
            removed=False
            break
    assert not removed, "should not remove if percentage is less than 1"
             
    
    
