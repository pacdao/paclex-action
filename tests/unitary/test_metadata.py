import brownie


def test_token_uri_ipfs(nft_minted):
    assert nft_minted.tokenURI(1)[0:7] == "ipfs://"


def test_mints_with_updated_metadata(nft, beneficiary, alice, leaf, proof):
    new_data = "new_uri"
    nft.setDefaultMetadata(new_data, {"from": beneficiary})
    nft.mint(leaf, proof, {"from": alice})
    assert nft.tokenURI(nft.totalSupply()) == nft.baseURI() + new_data


def test_new_beneficiary_can_update_metadata(nft, alice, bob, beneficiary, leaf, proof):
    founder = nft
    founder.updateBeneficiary(bob, {"from": beneficiary})
    new_data = "new uri"
    founder.setDefaultMetadata(new_data, {"from": bob})
    founder.mint(leaf, proof, {"from": alice})
    assert founder.tokenURI(founder.totalSupply()) == founder.baseURI() + new_data


def test_contract_uri(nft, contractURI):
    assert nft.contractURI() == contractURI


def test_token_default_uri(nft_minted, tokenURI):
    assert nft_minted.tokenURI(1) == tokenURI


def test_nonadmin_cannot_update_contract_uri(nft, accounts):
    with brownie.reverts("dev: Only Admin"):
        nft.setContractURI("test", {"from": accounts[2]})


def test_contract_uri_updates(nft, beneficiary):
    nft.setContractURI("test", {"from": beneficiary})
    assert nft.contractURI() == "ipfs://test"
