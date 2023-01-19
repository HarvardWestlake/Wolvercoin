#version ^0.3.7

import pytest
import brownie
from web3.exceptions import ValidationError



@pytest.fixture
def testVote(ExclusivityContract,accounts):
    #Exclusivity.deploy("0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000000", {'from': accounts[1]})
    #exclusivity: Exclusivity=Exclusivity()
    ExclusivityContract.classSize = 100
    ExclusivityContract.topicsAddress.append(accounts[0])
    ExclusivityContract.vote(accounts[0])
    valueChanged: bool=False
    if ExclusivityContract.balance(accounts[0])>=1:#balance thing may be source of error, needs to be a
            valueChanged = True
    assert valueChanged
    valueChanged = False
    
    ExclusivityContract.admin[accounts[0]] = True
    ExclusivityContract.vote(accounts[0])
    if ExclusivityContract.balance(accounts[0])>=16:
            valueChanged = True
    assert valueChanged
    

def testTally(ExclusivityContract,accounts):
    ExclusivityContract.percentage = 0.51
    ExclusivityContract.tallyVotes(accounts[0])
    
    removed: bool=True
    for studentAddress in ExclusivityContract.getTopicsList().return_value:
        if studentAddress==accounts[0]:
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



