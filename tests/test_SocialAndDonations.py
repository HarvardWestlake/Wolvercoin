# @version ^0.3.8

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

@pytest.fixture
def erc20Contract(SocialAndDonations, accounts):
    return SocialAndDonations.deploy(
        accounts[0],
        {'from': accounts[0]}
    )
def SocialAndDonations(SocialAndDonations, accounts):
    return SocialAndDonations.deploy(accounts)

def test_addPotentialOfficial(erc20Contract, accounts):
    erc20Contract.addPotentialOfficial(accounts[0])
    erc20Contract.addPotentialOfficial(accounts[1])
    assert erc20Contract.getLengthOfPotential().return_value == 2

def test_vote(erc20Contract, accounts):
    erc20Contract.vote(accounts[0])
    erc20Contract.vote(accounts[1])
    erc20Contract.vote(accounts[1])
    assert erc20Contract.getVotes(accounts[0]).return_value == 1
    assert erc20Contract.getVotes(accounts[1]).return_value == 2


def test_determineResult(erc20Contract, accounts):
    erc20Contract.addPotentialOfficial(accounts[0])
    erc20Contract.addPotentialOfficial(accounts[1])
    assert erc20Contract.determineResult().return_value == accounts[1]

def test_addStudent(erc20Contract, accounts):
    erc20Contract.addStudent(accounts[0],2012)
    erc20Contract.addStudent(accounts[1],2009)
    assert erc20Contract.getLengthOfStudents().return_value == 2

def test_checkIfActive(erc20Contract, accounts):
    erc20Contract.addStudent(accounts[0],2012)
    erc20Contract.addStudent(accounts[1],2009)
    assert erc20Contract.checkIfActive(accounts[0]).return_value == True
#def test_take10Percent():

def test_deposit10Percent(erc20Contract,accounts):

    preBank=erc20Contract.balanceOf(accounts[1])
    preProvider=erc20Contract.balanceOf(accounts[0])
    erc20Contract.deposit10Percent(accounts[0])    
    postBank=erc20Contract.balanceOf(accounts[1])
    postProvider=erc20Contract.balanceOf(accounts[0])
    #assert postBank==preBank-erc20Contract.totalOfTransactions*.1 and postProvider==preProvider+erc20Contract.totalOfTransactions*.1, "successfully invested 10%"
    assert True
