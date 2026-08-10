# Revenue Tracking — v4

**Purpose:** Log all REALIZED profit (money actually received, not projections).
**Rule:** Only on-chain verified revenue counts. v3 told the agent to "verify tips" but
provided no code. v4 enforces verification via the `revenue_verify` tool.

## Total Realized Profit (verified on-chain)

$0.00 (no tips received yet — agent should call `revenue_verify` periodically to check)

## Transaction Log

(Empty — agent will append verified transactions here)

| Date | Source | Amount | Currency | USD Value | Chain | Tx Hash |
|------|--------|--------|----------|-----------|-------|---------|
| —    | —      | —      | —        | —         | —     | —       |

## Crypto Wallets (Public Receive Addresses Only — Never Request Private Keys)

| Chain                | Address                                              | Free Verification API |
|----------------------|------------------------------------------------------|------------------------|
| Bitcoin (BTC)        | `bc1qh3areygq598ntxht0yp5yv87ej7g6aqvw8fl4z`        | blockchain.info/q/addressbalance/ |
| Ethereum / ERC-20    | `0xd6DFE6b54bF3dBC919Fde57009452fe6bbb0D997`        | api.etherscan.io/api?module=account&action=balance |
| Solana (SOL)         | `2emXSLoziaB5wdC8y48ovbu41agh9PzR5ro8o7kRDUvM`      | api.mainnet-beta.solana.com (getBalance) |
| Tron / USDT-TRC20    | `TJxkyJW57Tb8qmvvv5rCh3L2FYssRvWFEv`                | api.trongrid.io/v1/accounts/ |

## Other Revenue Channels (non-crypto)

| Channel | Status | Notes |
|---------|--------|-------|
| GitHub Sponsors | Pending setup | Operator must enable at https://github.com/sponsors/YOUR-USERNAME |
| Buy Me a Coffee | Pending setup | Operator must register at https://buymeacoffee.com |
| EthicalAds | Pending setup | Operator must register at https://ethicalads.io |
| Carbon Ads | Pending setup | Operator must apply at https://carbonads.net |
| Buttondown newsletter | Pending setup | Operator must create newsletter at https://buttondown.com |
| Affiliate programs | Pending setup | Operator must register for each: DigitalOcean, Vultr, Notion, etc. |

## Revenue Verification Rules

1. **On-chain only.** The agent must call `revenue_verify(chain)` to check the actual balance.
2. **Delta only.** Only the increase since last check counts as new revenue.
3. **Log immediately.** When `revenue_verify` returns a delta > 0, the agent should also
   emit a `revenue_update` field with the verified amount, which gets logged here.
4. **No projections.** "We expect to earn $X from this stream" is NOT revenue. Only realized.

## Notes

- Network fees are NOT subtracted from the tip amount (we receive net of fees).
- v3 logged $0.06 from "prior experiment" but never verified it on-chain. v4 starts fresh.
- The agent should check each chain at least once per day (rotating through chains).
