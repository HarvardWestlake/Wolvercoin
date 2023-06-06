#version ^0.3.7

# iris ref - [7] is voting address, [8] is lottery address, [9] is ricky c

import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def ExclusivityContract(Exclusivity, accounts):
    return Exclusivity.deploy("0xF1F6619B38A98d6De0800F1DefC0a6399eB6d30C", {'from': accounts[0]})

@pytest.fixture
def testVote(ExclusivityContract, accounts):

    ExclusivityContract.classSize = 100
    ExclusivityContract.topicsAddress.append(accounts[1])

    originalBalance: uint256 = accounts[1].balance

    ExclusivityContract.vote(accounts[0])

    if accounts[0].balance > originalBalance:
        valueChanged = True
    assert valueChanged
    valueChanged = False
    
    ExclusivityContract.admin[accounts[0]] = True
    ExclusivityContract.vote(accounts[0])
    if ExclusivityContract.balance(accounts[0]) >= 16:
        valueChanged = True
    assert valueChanged
    

def testTallyVotes(ExclusivityContract, accounts):
    ExclusivityContract.percentage = 0.51
    ExclusivityContract.tallyVotes(accounts[0])
    
    removed: bool = True
    for studentAddress in ExclusivityContract.getTopicsList().return_value:
        if studentAddress == accounts[0]:
            removed = False
            break
    assert removed

def testAddNonTopics(ExclusivityContract, accounts):
    ExclusivityContract.addToTopicsList(accounts[2])
    ExclusivityContract.setPercentage(100) # SET TO 20 FOR TEST TESTING, CHANGE TO 100 LATER
    ExclusivityContract.addNonTopics(accounts[1])

    assert ExclusivityContract.isInTopicsList(accounts[1]).return_value, "should add if percentage is 100 or greater"

    ExclusivityContract.popTopicList()
    ExclusivityContract.setPercentage(20)
    ExclusivityContract.addNonTopics(accounts[1])
    
    assert not ExclusivityContract.isInTopicsList(accounts[1]).return_value, "should not add if percentage is lower than 100"


def testRemoveTopics(ExclusivityContract, accounts):

    ExclusivityContract.addToTopicsList(accounts[2])
    ExclusivityContract.addToTopicsList(accounts[1])
    ExclusivityContract.addToTopicsList(accounts[3])
    ExclusivityContract.addToTopicsList(accounts[4])

    ExclusivityContract.setPercentage(100)
    ExclusivityContract.removeTopics(accounts[1])
    
    assert not ExclusivityContract.isInTopicsList(accounts[1]).return_value, "should remove if percentage is greater than or equal to 100"
    ExclusivityContract.addToTopicsList(accounts[1])

    ExclusivityContract.setPercentage(2)
    ExclusivityContract.removeTopics(accounts[1])
    assert ExclusivityContract.isInTopicsList(accounts[1]).return_value, "should not remove if percentage is less than 100"

def testAccounts(ExclusivityContract, accounts):
    f = open("account_test.txt", "w") 
    f.write("debug output for testAccounts in test_Exclusivity.py \n")
    f.write("adding to topics list: \n")
    s1 = ""

    for i in range(len(accounts)): 
        f.write(accounts[i].address + "\n")
        ExclusivityContract.addToTopicsList(accounts[i].address)
        s1 += accounts[i].address

    arr = ExclusivityContract.getTopicsList().return_value
    f.write("\n reading from topics list: ")
    s2 = ""

    for i in arr:
        s2 += i
        f.write(i + "\n")

    f.close()

    assert s1 == s2

