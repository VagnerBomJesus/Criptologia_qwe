from core import blockchain


def test_blockchain_add_action(tmp_path, monkeypatch):
    original = blockchain.BLOCKCHAIN_FILE
    file_path = tmp_path / "chain.json"
    monkeypatch.setattr(blockchain, "BLOCKCHAIN_FILE", str(file_path))

    blockchain.add_action("teste")
    chain = blockchain.get_chain()
    assert len(chain) == 1
    assert chain[0]["action"] == "teste"
    assert chain[0]["index"] == 0

    blockchain.add_action("outra")
    chain = blockchain.get_chain()
    assert len(chain) == 2
    assert chain[1]["prev_hash"] == chain[0]["hash"]

    blockchain.BLOCKCHAIN_FILE = original
