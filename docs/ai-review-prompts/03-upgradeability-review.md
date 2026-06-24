# AI Review Prompt: Upgradeability and Proxy Review

You are reviewing a Solidity project that may use proxies or upgradeable contracts.

Goal: identify upgradeability risks and documentation gaps before audit/mainnet.

Inputs to paste below:

- Solidity contracts
- Deployment scripts
- DLSK report
- Any proxy/admin addresses or deployment notes

## Review checklist

1. Detect UUPS, Transparent Proxy, Beacon Proxy, custom proxy, delegatecall, initializer, reinitializer, storage gaps, and implementation admin patterns.
2. Identify who can upgrade and how upgrades are authorized.
3. Check whether initialization appears protected.
4. Identify storage-layout or delegatecall areas that require expert audit.
5. Identify whether upgrade power is documented for users/investors/auditors.
6. Do not claim safety without manual verification.

## Output format

- Upgradeability summary
- Upgrade authority table
- Initialization concerns
- Storage/delegatecall concerns
- Launch blockers
- Questions for the team
