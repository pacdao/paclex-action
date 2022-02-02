from brownie import PACLEXAction


def test_non_beneficiary_can_deploy(alice, bob):
    PACLEXAction.deploy({"from": bob})
