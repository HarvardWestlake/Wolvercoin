#version ^0.3.7

# iris ref - [7] is voting address, [8] is lottery address, [9] is ricky c

import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def ExclusivityContract(Exclusivity, accounts):
    return Exclusivity.deploy("0xF1F6619B38A98d6De0800F1DefC0a6399eB6d30C", {'from': accounts[0]})

def testVote(ExclusivityContract, accounts):
    ExclusivityContract.classSize = 100

    # test with admin
    valueChanged: bool = False
    ExclusivityContract.makeAdmin(accounts[0])
    ExclusivityContract.vote(accounts[0])
    if accounts[0].balance() >= 16:
        valueChanged = True
    assert valueChanged

    # test with regular student
    ExclusivityContract.addToTopicsList(accounts[1])

    try:
        ExclusivityContract.vote(accounts[1])
    except brownie.exceptions.VirtualMachineError:
        pass

    if accounts[1].balance() > 0:
        valueChanged = True
    assert valueChanged


def testTallyVotes(ExclusivityContract, accounts):
    ExclusivityContract.addToTopicsList(accounts[0])
    ExclusivityContract.addToTopicsList(accounts[1])

    # test above 0.5 - should remove
    ExclusivityContract.setPercentage(51)
    assert ExclusivityContract.tallyVotes(accounts[0]).return_value

    # test below 0.5 - shouldn't remove
    ExclusivityContract.setPercentage(40)
    assert not ExclusivityContract.tallyVotes(accounts[1]).return_value

def testAddNonTopics(ExclusivityContract, accounts):
    # test successfully add case 
    ExclusivityContract.setPercentage(100)
    ExclusivityContract.addNonTopics(accounts[1])

    assert ExclusivityContract.isInTopicsList(accounts[1]).return_value, "should add if percentage is 100 or greater"

    # test fail to add case
    ExclusivityContract.setPercentage(20)
    ExclusivityContract.addNonTopics(accounts[2])
    
    assert not ExclusivityContract.isInTopicsList(accounts[2]).return_value, "should not add if percentage is lower than 100"


def testRemoveTopics(ExclusivityContract, accounts):

    ExclusivityContract.addToTopicsList(accounts[2])
    ExclusivityContract.addToTopicsList(accounts[1])
    ExclusivityContract.addToTopicsList(accounts[3])
    ExclusivityContract.addToTopicsList(accounts[4])

    # f = open("account_test.txt", "w") 
    # for adr in ExclusivityContract.getTopicsList().return_value:
    #     f.write(adr)
    #     f.write("\n")
    # f.write("\n trying remove 1")

    ExclusivityContract.setPercentage(100)

    removed_success: bool = ExclusivityContract.removeTopics(accounts[1]).return_value
    
    assert removed_success, "should remove if percentage is greater than or equal to 100"

    removed_success = False

    # for adr in ExclusivityContract.getTopicsList().return_value:
    #     f.write(adr)
    #     f.write("\n")
    # f.write("\n trying remove 2")

    ExclusivityContract.setPercentage(2)

    removed_success = ExclusivityContract.removeTopics(accounts[2]).return_value
    
    # for adr in ExclusivityContract.getTopicsList().return_value:
    #     f.write(adr)
    #     f.write("\n")
    # f.close()

    assert not removed_success, "should not remove if percentage is less than 100"


def testWithdraw(ExclusivityContract, accounts): 
    ExclusivityContract.addToTopicsList(accounts[1])

    assert ExclusivityContract.withdraw(100, accounts[1]).return_value == (100, "nice")
    try: 
        assert ExclusivityContract.withdraw(100, accounts[2]).return_value == (50, "should've taken topics")
    except brownie.exceptions.VirtualMachineError:
        pass
    
    try:
        assert ExclusivityContract.withdraw(100, accounts[9]).return_value == (5, "Enjoy your joyful pursuit of education!")
    except brownie.exceptions.VirtualMachineError:
        pass

# def testAccounts(ExclusivityContract, accounts):
#     f = open("account_test.txt", "a") 
#     f.write("debug output for testAccounts in test_Exclusivity.py \n")
#     f.write("adding to topics list: \n")
#     s1 = ""

#     for i in range(len(accounts)): 
#         f.write(accounts[i].address + "\n")
#         ExclusivityContract.addToTopicsList(accounts[i].address)
#         s1 += accounts[i].address

#     arr = ExclusivityContract.getTopicsList().return_value
#     f.write("\n reading from topics list: ")
#     s2 = ""

#     for i in arr:
#         s2 += i
#         f.write(i + "\n")

#     f.close()

#     assert s1 == s2

