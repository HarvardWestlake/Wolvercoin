#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def ExclusivityContract(Exclusivity, accounts):
    return Exclusivity.deploy({'from': accounts[0]})
    
# def testVote(ExclusivityContract):
#     ExclusivityContract.classSize = 100
#     ExclusivityContract.topicsAddress.append(0xf34b09E22f5115af490eeb7460304aB80c90399E)
#     ExclusivityContract.vote(0xf34b09E22f5115af490eeb7460304aB80c90399E)
#     valueChanged: bool=False
#     if balance(0xf34b09E22f5115af490eeb7460304aB80c90399E)>=1: #what's balance()?
#         valueChanged = True
#     assert valueChanged
#     valueChanged = False
    
#     ExclusivityContract.admin[0xf34b09E22f5115af490eeb7460304aB80c90399E] = True
#     ExclusivityContract.vote(0xf34b09E22f5115af490eeb7460304aB80c90399E)
#     if balance(0xf34b09E22f5115af490eeb7460304aB80c90399E)>=16:
#         valueChanged = True
#     assert valueChanged

# def testTally(ExclusivityContract):
   
#     ExclusivityContract.percentage = 0.51
#     ExclusivityContract.tallyVotes(0xf34b09E22f5115af490eeb7460304aB80c90399E)
    
#     removed: bool=True
#     for studentAddress in ExclusivityContract.topicsAddress:
#         if studentAddress==0xf34b09E22f5115af490eeb7460304aB80c90399E:
#             removed = False
#             break
    
#     assert removed
    
def testAddNonTopics(ExclusivityContract, accounts):
    
    ExclusivityContract.percentage=1
    ExclusivityContract.addNonTopics(accounts[1])
    added: bool=False
    for studentAddress in ExclusivityContract.topicsAddress:
        if studentAddress==accounts[1]:
            added=True
            break
    assert added,"should add if percentage is 1 or greater"

    ExclusivityContract.topicsAddress.pop()
    ExclusivityContract.percentage=0.2
    ExclusivityContract.addNonTopics(accounts[1])
    added=False
    for studentAddress in ExclusivityContract.topicsAddress:
        if studentAddress==accounts[1]:
            added=True
            break 
    assert not added,"should not add if percentage is lower than 1"
    


def testRemoveTopics(ExclusivityContract,accounts):

    ExclusivityContract.addToTopicsList(accounts[1])
    ExclusivityContract.percentage=1
    ExclusivityContract.removeNonTopics(accounts[1])
    removed: bool=True
    for studentAddress in ExclusivityContract.topicsAddress:
        if studentAddress==accounts[1]:
            removed=False
            break
    assert removed, "should remove if percentage is greater than or equal to 1"

    ExclusivityContract.addToTopicsList(accounts[1])
    ExclusivityContract.percentage=0.2
    ExclusivityContract.removeNonTopics(accounts[1])
    removed=True
    for studentAddress in ExclusivityContract.topicsAddress:
        if studentAddress==accounts[1]:
            removed=False
            break
    assert not removed, "should not remove if percentage is less than 1"
             
    
    

