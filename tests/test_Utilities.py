def utilitiesContract (Utilities, accounts) #accounts is bc someone needs to pay for contract
    return Utilities.deploy ({'from':accounts[0]})

def test_redeemProduct(utilitiesContract, accounts):
    with pytest.raises(Exception) as e_info:
        utilitiesContract.redeemProduct(2)