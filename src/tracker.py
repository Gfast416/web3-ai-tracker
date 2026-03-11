"""
web3-ai-tracker/src/tracker.py
On-chain data fetching via Etherscan API
"""
import os
import requests
from dataclasses import dataclass
from typing import Optional

ETHERSCAN_API = "https://api.etherscan.io/api"


@dataclass
class Transaction:
    hash: str
    from_addr: str
    to_addr: str
    value_eth: float
    token_symbol: Optional[str]
    timestamp: int
    is_contract_interaction: bool


def get_wallet_transactions(wallet: str, limit: int = 20) -> list[Transaction]:
    """Fetch recent transactions for a wallet address."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": limit,
        "sort": "desc",
        "apikey": os.getenv("ETHERSCAN_API_KEY"),
    }
    response = requests.get(ETHERSCAN_API, params=params, timeout=10)
    data = response.json()

    if data["status"] != "1":
        return []

    txs = []
    for tx in data["result"]:
        txs.append(Transaction(
            hash=tx["hash"],
            from_addr=tx["from"],
            to_addr=tx["to"],
            value_eth=int(tx["value"]) / 1e18,
            token_symbol=None,
            timestamp=int(tx["timeStamp"]),
            is_contract_interaction=bool(tx.get("input") and tx["input"] != "0x"),
        ))
    return txs


def get_token_transfers(wallet: str, limit: int = 20) -> list[dict]:
    """Fetch ERC-20 token transfer events."""
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet,
        "page": 1,
        "offset": limit,
        "sort": "desc",
        "apikey": os.getenv("ETHERSCAN_API_KEY"),
    }
    response = requests.get(ETHERSCAN_API, params=params, timeout=10)
    data = response.json()

    if data["status"] != "1":
        return []

    return [
        {
            "token": tx["tokenSymbol"],
            "value": int(tx["value"]) / (10 ** int(tx["tokenDecimal"])),
            "from": tx["from"],
            "to": tx["to"],
            "contract": tx["contractAddress"],
            "hash": tx["hash"],
        }
        for tx in data["result"]
    ]


def is_whale_movement(tx: Transaction, threshold_eth: float = 10.0) -> bool:
    """Flag transactions above whale threshold."""
    return tx.value_eth >= threshold_eth