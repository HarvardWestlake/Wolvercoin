#version ^0.3.7

import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def exclusivityContract(Exclusivity, accounts):
    return Exclusivity.deploy("0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", {'from': accounts[1]})


def testVote(Exclusivity,accounts):
    Exclusivity.deploy("0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", {'from': accounts[1]})
    exclusivity: Exclusivity=Exclusivity()
    Exclusivity.classSize = 100
    exclusivity.topicsAddress.append(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    exclusivity.vote(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    valueChanged: bool=False
    if balance(0xf34b09E22f5115af490eeb7460304aB80c90399E)>=1:#balance thing may be source of error, needs to be a
            valueChanged = True
    assert valueChanged
    valueChanged = False
    
    exclusivity.admin[0xf34b09E22f5115af490eeb7460304aB80c90399E] = True
    exclusivity.vote(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    if balance(0xf34b09E22f5115af490eeb7460304aB80c90399E)>=16:
            valueChanged = True
    assert valueChanged
    

def testTally(Exclusivity,accounts):
    Exclusivity.deploy("0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", {'from': accounts[1]})
    #Exclusivity: Exclusivity=Exclusivity()
    Exclusivity.percentage = 0.51
    Exclusivity.tallyVotes(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    
    removed: bool=True
    for studentAddress in Exclusivity.topicsAddress:
        if studentAddress==0xf34b09E22f5115af490eeb7460304aB80c90399E:
            removed = False
            break
    assert removed
    

@pytest.fixture
def ExclusivityContract(Exclusivity, accounts):
    return Exclusivity.deploy({'from': accounts[0]})

def testAddNonTopics(ExclusivityContract, accounts):
    ExclusivityContract.addToTopicsList(accounts[2])
    ExclusivityContract.setPercentage(100)
    ExclusivityContract.addNonTopics(accounts[1])
    
    assert ExclusivityContract.isInTopicsList(accounts[1]),"should add if percentage is 100 or greater"

    ExclusivityContract.popTopicList()
    ExclusivityContract.setPercentage(20)
    ExclusivityContract.addNonTopics(accounts[1])
    
    assert  ExclusivityContract.isNotinTopicsList(accounts[1]),"should not add if percentage is lower than 100"

def testRemoveTopics(ExclusivityContract,accounts):
    ExclusivityContract.addToTopicsList(accounts[2])
    ExclusivityContract.addToTopicsList(accounts[1])
    ExclusivityContract.setPercentage(100)
    ExclusivityContract.removeNonTopics(accounts[1])
    
    assert ExclusivityContract.isNotinTopicsList(accounts[1]), "should remove if percentage is greater than or equal to 1"
    ExclusivityContract.addToTopicsList(accounts[1])

    ExclusivityContract.setPercentage(100)
    ExclusivityContract.removeNonTopics(accounts[1])
    assert ExclusivityContract.isInTopicsList(accounts[1]), "should not remove if percentage is less than 1"



