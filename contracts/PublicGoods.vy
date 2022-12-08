# @version ^0.3.7

struct Donation:
    donator: address
    amount: decimal

struct Good:
    name: String[50]
    goal: decimal
    donations: Donation[50] # Up to 50 people can donate to a good
    totalDonations: decimal

goods: public(HashMap[String[50], Good]) # There can be up to 50 goods collecting donations

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

    # Change from tech spec: donations are stored as an array of Donation objects
    # Loop through the donations array, find the address of the donation associated
    # with the donator, and increment the value. If user has no associated donation
    # object, create one
    return

@external
def retract(name: String[50], amount: decimal):
    # TODO for @monkeymatt2023

    # See comment above
    return

@external
def complete(name: String[50]):
    # TODO for @ericyoondotcom
    return
