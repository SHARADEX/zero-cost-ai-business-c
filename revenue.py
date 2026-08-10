#!/usr/bin/env python3
"""
Revenue verification — v4 NEW module
====================================

v3 told the agent to "verify tips" but provided no code to enforce it.
v4 has actual on-chain balance checks.

Supported chains:
  - Bitcoin  — blockchain.info balance API (free, no key)
  - Ethereum — etherscan.io API (free, no key for low volume)
  - Solana   — mainnet-beta RPC getBalance (free)
  - Tron     — trongrid.io account API (free)
  - Ronin    — skipped (Ronin doesn't have a free public API; manual check)

The agent calls revenue_verify("ethereum") etc. The module fetches the current
balance, compares to the last-logged balance, and returns the delta in native units.

If delta > 0, that's a confirmed tip. The agent should then log it to revenue.md.
"""

import os
import json
import urllib.request
from typing import Tuple, Optional
from datetime import datetime, timezone

REVENUE_FILE = "memory/revenue.md"
REVENUE_JSON = "memory/revenue_ledger.json"

# Public receive addresses (operator must replace with their own)
WALLETS = {
    "bitcoin":   "bc1qh3areygq598ntxht0yp5yv87ej7g6aqvw8fl4z",
    "ethereum":  "0xd6DFE6b54bF3dBC919Fde57009452fe6bbb0D997",
    "ronin":     "0xAa4E76e5Be5334c0f2Fe0716C42B2FC61D4c150B",
    "solana":    "2emXSLoziaB5wdC8y48ovbu41agh9PzR5ro8o7kRDUvM",
    "tron":      "TJxkyJW57Tb8qmvvv5rCh3L2FYssRvWFEv",
}

# Approximate USD prices, refreshed periodically (fallback if API fails)
FALLBACK_PRICES = {
    "bitcoin":  65000.0,
    "ethereum": 3200.0,
    "solana":   150.0,
    "tron":     0.13,
    "ronin":    1.20,
}


def _read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return default


def _write_json(path, data):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _get_json(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def _get_text(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "ZeroCostAI/4.0"}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_balance(chain: str) -> Optional[float]:
    """Fetch current balance in native units. Returns None on error."""
    chain = chain.lower()
    addr = WALLETS.get(chain)
    if not addr:
        return None
    try:
        if chain == "bitcoin":
            # blockchain.info returns satoshis
            txt = _get_text(f"https://blockchain.info/q/addressbalance/{addr}")
            satoshis = int(txt.strip())
            return satoshis / 1e8
        elif chain == "ethereum":
            # Etherscan free API (no key, rate-limited)
            data = _get_json(
                f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest"
            )
            wei = int(data.get("result", "0"))
            return wei / 1e18
        elif chain == "solana":
            # Solana mainnet RPC getBalance
            payload = json.dumps({
                "jsonrpc": "2.0", "id": 1,
                "method": "getBalance",
                "params": [addr]
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.mainnet-beta.solana.com",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
            lamports = data.get("result", {}).get("value", 0)
            return lamports / 1e9
        elif chain == "tron":
            # TronGrid get account
            data = _get_json(f"https://api.trongrid.io/v1/accounts/{addr}")
            balance_sun = 0
            for token_data in data.get("data", []):
                balance_sun += int(token_data.get("balance", 0))
            return balance_sun / 1e6  # Convert sun to TRX
        elif chain == "ronin":
            # No free public API — return None, agent should ask human
            return None
    except Exception as e:
        # Log error to stderr (caller can log it to blocked.md)
        print(f"[revenue] Failed to fetch {chain} balance: {e}")
        return None


def fetch_price_usd(chain: str) -> Optional[float]:
    """Fetch current USD price. Returns None on error."""
    chain = chain.lower()
    # Map to coingecko ids
    cg_ids = {
        "bitcoin": "bitcoin",
        "ethereum": "ethereum",
        "solana": "solana",
        "tron": "tron",
        "ronin": "ronin",
    }
    cg_id = cg_ids.get(chain)
    if not cg_id:
        return FALLBACK_PRICES.get(chain)
    try:
        data = _get_json(
            f"https://api.coingecko.com/api/v3/simple/price?ids={cg_id}&vs_currencies=usd"
        )
        return data.get(cg_id, {}).get("usd", FALLBACK_PRICES.get(chain))
    except Exception:
        return FALLBACK_PRICES.get(chain)


def verify_chain(chain: str) -> dict:
    """
    Verify a chain's balance, compare to last logged balance, return delta.

    Returns dict with:
      - chain, current_balance, last_balance, delta, delta_usd, price_usd, error
    """
    chain = chain.lower()
    current = fetch_balance(chain)
    if current is None:
        return {
            "chain": chain,
            "current_balance": None,
            "last_balance": None,
            "delta": None,
            "delta_usd": None,
            "price_usd": None,
            "error": f"Failed to fetch balance for {chain}"
        }

    ledger = _read_json(REVENUE_JSON, {"last_balances": {}, "transactions": []})
    last_balance = ledger.get("last_balances", {}).get(chain, 0.0)
    delta = current - last_balance
    price = fetch_price_usd(chain)
    delta_usd = delta * price if (price and delta > 0) else 0.0

    # Update ledger
    ledger.setdefault("last_balances", {})[chain] = current
    if delta > 0:
        ledger.setdefault("transactions", []).append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "chain": chain,
            "amount_native": delta,
            "amount_usd": delta_usd,
            "price_usd": price,
            "verified": True,
            "source": "on-chain",
        })
    _write_json(REVENUE_JSON, ledger)

    return {
        "chain": chain,
        "current_balance": current,
        "last_balance": last_balance,
        "delta": delta,
        "delta_usd": delta_usd,
        "price_usd": price,
        "error": None,
    }


def get_total_realized_usd() -> float:
    """Sum of all verified on-chain transactions in USD."""
    ledger = _read_json(REVENUE_JSON, {"transactions": []})
    return sum(t.get("amount_usd", 0) for t in ledger.get("transactions", []))
