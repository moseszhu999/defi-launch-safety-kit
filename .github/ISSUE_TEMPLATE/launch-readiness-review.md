---
name: Launch-readiness review request
about: Request a lightweight pre-audit / launch-readiness review
title: "Launch-readiness review: <project name>"
labels: ["launch-readiness", "review-request"]
assignees: []
---

## Project summary

Please describe the project in 2-5 sentences.

- Project name:
- Website / docs:
- Repository URL:
- Target chain(s):
- Expected launch stage: testnet / audit preparation / mainnet / already live

## Contract scope

List the contracts that should be reviewed.

```text
contracts/Token.sol
contracts/Staking.sol
contracts/Vesting.sol
```

## Project type

Select all that apply:

- [ ] ERC20 token
- [ ] Staking
- [ ] Vesting
- [ ] Airdrop
- [ ] Treasury / multisig operations
- [ ] Upgradeable contracts
- [ ] Other:

## What you want checked

Select all that apply:

- [ ] Owner/admin privilege review
- [ ] Mint/burn authority
- [ ] Pause / blacklist / whitelist controls
- [ ] Tax / fee / transfer controls
- [ ] Rescue / sweep / emergency withdraw paths
- [ ] Upgradeability / proxy surface
- [ ] Contract surface map
- [ ] Foundry / Hardhat readiness
- [ ] Deployment script readiness
- [ ] CI / SARIF security gate readiness
- [ ] Audit-preparation pack

## Current readiness

- Tests available? yes / no / partial
- Deployment scripts available? yes / no / partial
- CI workflow available? yes / no / partial
- Coverage artifacts available? yes / no / partial
- Previous audit? yes / no / planned

## Known concerns

Please list anything the team already knows is risky or unfinished.

```text
Example:
- owner can mint before launch
- staking reward parameters are still adjustable
- rescue function is intended for non-core tokens only
```

## Constraints

- Desired review depth: quick triage / detailed pre-audit / CI setup
- Preferred output: Markdown / HTML / JSON / SARIF / audit-prep pack
- Timeline:

## Important disclaimer

This request is for lightweight pre-audit and launch-readiness triage. It is not a formal security audit and does not guarantee the absence of vulnerabilities.
