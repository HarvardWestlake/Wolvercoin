# @version ^0.3.7

struct Good:
    name: String[50]
    goal: decimal
    donations: HashMap[address, decimal]
    totalDonations: decimal

goods: public(HashMap[String[50], Good])

@external
def __init__():
    # Empty
    return

@external
def createGood(name: String[50], goal: decimal):
    # TODO for @exoskeleton-1729
    
    # Note change from tech spec made by @ericyoondotcom 2022-12-08: goods is now a hashmap
    # The key of the hashmap is the name of the good
    return

@external
def contribute(name: String[50], amount: decimal):
    # TODO for @stevenk8819
    return

@external
def retract(name: String[50], amount: decimal):
    # TODO for @monkeymatt2023
    return

@external
def complete(name: String[50]):
    # TODO for @ericyoondotcom
    return
