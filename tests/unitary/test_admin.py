import brownie


def test_new_beneficiary_can_receive(nft_minted, beneficiary, alice, bob):
    nft_minted.updateBeneficiary(bob, {"from": beneficiary})
    bob_init = bob.balance()
    nft_minted.withdraw({"from": alice})
    assert bob.balance() >= bob_init


def test_new_beneficiary_can_withdraw(nft_minted, alice, bob, beneficiary, accounts):
    accounts[0].transfer(nft_minted, 10 ** 18)
    nft_minted.updateBeneficiary(bob, {"from": beneficiary})
    bob_init = bob.balance()
    nft_minted.withdraw({"from": bob})
    assert bob.balance() > bob_init


def test_nonowner_cannot_transfer_owner(nft_minted, alice, bob):
    with brownie.reverts():
        nft_minted.updateBeneficiary(bob, {"from": bob})


def test_new_beneficiary_can_update_beneficiary(
    nft_minted, alice, bob, beneficiary, accounts
):
    nft_minted.updateBeneficiary(bob, {"from": beneficiary})
    nft_minted.updateBeneficiary(alice, {"from": bob})
    accounts[3].transfer(nft_minted, 10 ** 18)
    alice_init = alice.balance()
    nft_minted.withdraw({"from": bob})
    assert alice.balance() > alice_init


def test_fallback_receivable(nft, alice, accounts):
    founder_init = nft.balance()
    accounts[1].transfer(nft, 10 ** 18)
    assert nft.balance() - founder_init == 10 ** 18


def test_fallback_funds_withdrawable(nft, beneficiary, bob, accounts):
    founder_init = nft.balance()
    accounts[0].transfer(nft, 10 ** 18)
    beneficiary_init = beneficiary.balance()
    nft.withdraw({"from": beneficiary})
    assert beneficiary.balance() - beneficiary_init == 10 ** 18 + founder_init


def test_set_token_uri(nft_minted, beneficiary):
    string = "test"
    nft_minted.setTokenUri(1, string, {"from": beneficiary})
    assert nft_minted.tokenURI(1) == nft_minted.baseURI() + string


def test_non_admin_cannot_mint_for(nft, accounts):
    with brownie.reverts("Only Admin"):
        nft.mintFor(accounts[1], {"from": accounts[2]})
    assert nft.balanceOf(accounts[1]) == 0


def test_admin_can_mint_for(nft, accounts, beneficiary):
    nft.mintFor(accounts[1], {"from": beneficiary})
    assert nft.balanceOf(accounts[1]) == 1


def test_non_admin_cannot_set_token_uri(nft_minted, bob):
    init_uri = nft_minted.tokenURI(1)
    string = "test"
    with brownie.reverts("Only Admin"):
        nft_minted.setTokenUri(1, string, {"from": bob})
    assert nft_minted.tokenURI(1) == init_uri


def test_non_admin_cannot_update_merkle_root(nft, bob):
    with brownie.reverts("Only Admin"):
        nft.updateRoot(
            "0x0000000000000000000000000000000000000000000000000000000000000000",
            {"from": bob},
        )


def test_admin_can_update_merkle_root(nft, beneficiary, leaf, proof, bob):
    nft.updateRoot(
        "0x0000000000000000000000000000000000000000000000000000000000000000",
        {"from": beneficiary},
    )
    with brownie.reverts():
        nft.mint(leaf, proof, {"from": bob})
