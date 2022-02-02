import brownie


def test_merkle_mints(nft, bob, leaf, proof):
    with brownie.reverts():
        nft.ownerOf(1)
    nft.mint(leaf, proof, {"from": bob})
    assert nft.ownerOf(1) == bob


def test_merkle_remint_fails(nft, bob, leaf, proof):
    nft.mint(leaf, proof, {"from": bob})
    with brownie.reverts("dev: Leaf already used"):
        nft.mint(leaf, proof, {"from": bob})


def test_merkle_remint_suceeds_after_cap_raised(nft, beneficiary, bob, leaf, proof):
    assert nft.balanceOf(bob) == 0
    nft.mint(leaf, proof, {"from": bob})
    nft.updateMaxMintsPerLeaf(2, {"from": beneficiary})
    nft.mint(leaf, proof, {"from": bob})
    assert nft.balanceOf(bob) == 2


def test_cannot_mint_after_stop(nft, beneficiary, bob, leaf, proof):
    nft.updatePublicMint(False, {"from": beneficiary})
    with brownie.reverts():
        nft.mint(leaf, proof, {"from": bob})


def test_beneficiary_can_mint_for(nft, beneficiary, bob):
    nft.mintFor(bob, {"from": beneficiary})
    assert nft.ownerOf(1) == bob


def test_id_updates_on_mint_for(nft, beneficiary, bob):
    assert nft.balanceOf(bob) == 0
    first_id = nft.currentId()
    nft.mintFor(bob, {"from": beneficiary})
    assert nft.balanceOf(bob) > 0
    assert nft.currentId() == first_id + nft.balanceOf(bob)


def test_id_updates_on_mint(nft, bob, leaf, proof):
    assert nft.balanceOf(bob) == 0
    first_id = nft.currentId()
    nft.mint(leaf, proof, {"from": bob})
    assert nft.balanceOf(bob) > 0
    assert nft.currentId() > first_id + nft.balanceOf(bob)


def test_mint_gets_to_artist(nft, beneficiary, leaf, proof):
    assert nft.balanceOf(nft.artist()) == 0
    nft.updateMaxMintsPerLeaf(20, {"from": beneficiary})
    for i in range(20):
        nft.mint(leaf, proof, {"from": beneficiary})
    assert nft.balanceOf(nft.artist()) == 1


def test_sponsors_get_twelve(nft, beneficiary, leaf, proof, bob):
    assert nft.balanceOf(nft.pacdao()) == 0
    assert nft.balanceOf(nft.lexarmy()) == 0
    nft.updateMaxMintsPerLeaf(50, {"from": beneficiary})
    for i in range(50):
        nft.mint(leaf, proof, {"from": bob})
    assert nft.balanceOf(nft.pacdao()) == 12
    assert nft.balanceOf(nft.lexarmy()) == 12
