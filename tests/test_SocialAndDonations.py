import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()


def test_determineResult(socialAndDonationsContract):
    length = len(socialAndDonationsContract.electedOfficials)
    socialAndDonationsContract.determineResult()
    assert len(socialAndDonationsContract.electedOfficials) == length + 1, "New official successfully elected"
 