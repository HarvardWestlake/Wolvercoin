# @version 0.3.7

# WIP this doesnt work, but like in theory <3 
import eth-crypto as ec

def random_number(seed: bytes32) -> uint256:
    return ec.ecrecover(seed, 0, 0, 0, 0)














