from brownie import ZERO_ADDRESS, PACLEXAction, accounts, network
from brownie.network import max_fee, priority_fee


def main():
    publish_source = True
    multisig = "0xf27AC88ac7e80487f21e5c2C847290b2AE5d7B8e"
    beneficiary_address = multisig

    if network.show_active() in ["development"]:
        deployer = accounts[0]
        publish_source = False
        beneficiary_address = deployer

    elif network.show_active() in ["rinkeby", "ropsten"]:
        deployer = accounts.load("husky")
        beneficiary_address = deployer
        publish_source = True

    elif network.show_active() == "mainnet-fork":
        publish_source = False
        deployer = accounts[0]

    elif network.show_active() == "mainnet":
        deployer = accounts.load("minnow")
        max_fee(input("Max fee in gwei: ") + " gwei")
        priority_fee("2 gwei")
        publish_source = True

    else:
        deployer = accounts.load("husky")
        publish_source = True

    return PACLEXAction.deploy(
        {"from": deployer}, publish_source=publish_source
    )
