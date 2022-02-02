#!/usr/bin/python3

import pytest
from brownie import PACLEXAction


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def alice(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def bob(accounts):
    return accounts[1]


@pytest.fixture(scope="module")
def charlie(accounts):
    return accounts[2]


@pytest.fixture(scope="module")
def owner(accounts, nft):
    return accounts.at(nft.owner(), force=True)


@pytest.fixture(scope="module")
def nft(alice):
    return PACLEXAction.deploy({"from": alice})


@pytest.fixture(scope="module")
def leaf():
    return "0x001b0a4ba5dd8bf88653c3dd60b3298bc828f13843af9744f34f24f24b1ffb5f"


@pytest.fixture(scope="module")
def proof():
    return [
        "0x0056aa76e87594248547418b37040ea3f4c6232d80816a09bb111c6297f027c7",
        "0xa0d99f609735c73414db67879e2d19bb6ccf6b5da2e5864b324390c58e6220e9",
        "0x276b2fb9e9f28850eaf1c65b94607a3fd389f0ca46ab1ee7f79efcd7d58d2cd3",
        "0xe50e3175312020349c92f6575b5e025806ed476b6cbe28b4885da32144fe8e31",
        "0x21eefc1ddfcd161d4255773bc4e1b695d1dd700c04fe6642491d36165b2377af",
        "0x45667768cc8d3cd67615477187ea0f9e794e18b0c26215454b08878472572fb1",
        "0xdadbb99ab876a9bf690d6ea43c2ff8b880cc0988691b4a17d42c2cf92f72685a",
        "0xbc9a8af663027f6a9febfbb77a07ed4c69a668db9b5f44cc3bdaf4f0c49db5fb",
        "0x4b106e2dd3174a8b9d51ea198d1713699cf90283e4d74015040f0bed4e3ae38a",
        "0xaf0f1db5b8143f91e3b15a6026ca6abe935d1d476faa8e7120cf7454ca7ec996",
    ]


@pytest.fixture(scope="function")
def nft_minted(nft, alice, bob, beneficiary):
    nft.mintFor(alice, {"from": beneficiary})
    nft.mintFor(bob, {"from": beneficiary})
    return nft


@pytest.fixture(scope="function")
def nft_funded(nft, accounts):
    accounts[1].transfer(nft, 10 ** 18)
    return nft


@pytest.fixture(scope="function")
def beneficiary(nft, accounts):
    return accounts.at(nft.beneficiary(), force=True)


@pytest.fixture(scope="module")
def contractURI():
    return "ipfs://Qma4VAp8giZ74Ny7jJVW1e5V8kmC5VVaSeF6cbXWFizxsr"


@pytest.fixture(scope="module")
def tokenURI():
    return "ipfs://QmTYvCgKunY8W18kSpCK5eUpHSEzGCmzqQp185AU451ALV"
