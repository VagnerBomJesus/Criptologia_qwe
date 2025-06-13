import json
import os
import time
from typing import List, Dict

BLOCKCHAIN_FILE = "assets/blockchain.json"


def _load_chain() -> List[Dict]:
    if not os.path.exists(BLOCKCHAIN_FILE):
        return []
    with open(BLOCKCHAIN_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_chain(chain: List[Dict]) -> None:
    os.makedirs(os.path.dirname(BLOCKCHAIN_FILE), exist_ok=True)
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)


def _hash_block(block: Dict) -> str:
    data = f"{block['index']}{block['timestamp']}{block['action']}{block['prev_hash']}"
    return str(abs(hash(data)))


def add_action(action: str) -> None:
    chain = _load_chain()
    index = len(chain)
    prev_hash = chain[-1]["hash"] if chain else "0"
    block = {
        "index": index,
        "timestamp": time.time(),
        "action": action,
        "prev_hash": prev_hash,
    }
    block["hash"] = _hash_block(block)
    chain.append(block)
    _save_chain(chain)


def get_chain() -> List[Dict]:
    return _load_chain()
