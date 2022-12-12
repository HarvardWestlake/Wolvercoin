# @version 0.3.6

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

@pytest.fixture
def votingContract(VotingAndRep, accounts):
    return VotingAndRep.deploy({'from': accounts[0]})

def test_determineResult(socialAndDonationsContract):
    length = len(socialAndDonationsContract.electedOfficials)
    socialAndDonationsContract.determineResult()
    assert len(socialAndDonationsContract.electedOfficials) == length + 1, "New official successfully elected"
 