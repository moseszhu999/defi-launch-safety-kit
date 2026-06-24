# First Target Candidates — 2026-06-24

This is the first raw candidate list for the 14-day marketing experiment.

These are not endorsed projects and have not been contacted. They are public GitHub repositories found through keyword searches such as ERC20, Solidity, Hardhat, Foundry, staking, airdrop, and NFT marketplace.

Before outreach, each target must be manually checked for:

- credible project intent
- recent activity
- public Solidity contracts
- open issue/discussion/contact path
- no obvious scam/yield/pump-token positioning
- no existing formal audit report that makes a lightweight readiness pass redundant
- useful launch-readiness surface such as owner/admin controls, mint/pause/fee/tax, upgradeability, deployment scripts, tests, CI, or audit-prep gaps

Do not message all candidates. First shortlist 5.

---

## Candidate batch 1

| # | Repository | Type guess | Why it may fit | First action |
|---|---|---|---|---|
| 1 | `ArvinFarrelP/arvin-erc20-token` | ERC20 token | Small ERC20 token repo; likely simple launch-readiness surface | Check README, contracts, owner/mint/pause surface |
| 2 | `orien7/uday-erc20-staking` | ERC20 staking | Staking logic is a good fit for pre-audit checklist | Check staking contract, reward assumptions, tests |
| 3 | `qryptalabs/qrypta-token` | Token | Token repo under a named lab/team account | Check token controls, docs, contact path |
| 4 | `mooncitydev/eth-token-claim-contract` | Claim / airdrop-like | Token claim logic can benefit from readiness notes | Check claim authorization and deployment notes |
| 5 | `kiragami27/erc20-token` | ERC20 token | Simple token repo, likely useful as a lightweight demo candidate | Check if real project or learning repo |
| 6 | `ShamratDev/ERC20-Token-Hardhat-Multi-Network` | ERC20 / Hardhat | Multi-network Hardhat token repo; deployment readiness angle | Check deployment scripts and network config |
| 7 | `tudelachristian7/staking-dapp-solidity` | Staking dApp | Staking dApp; may have owner/reward/withdrawal surface | Check code depth and contact path |
| 8 | `eljavis/Staking-App` | Staking app | Staking app candidate, but repo appears small | Check whether enough code exists |
| 9 | `saurabh0829/merkle-airdrop-dapp` | Merkle airdrop | Airdrop projects fit launch-readiness review well | Check merkle proof, claim, admin, deployment docs |
| 10 | `gonzalolater/NFT-Marketplace-Solidity-Hardhat-NexJS-Web3js-Tailwind` | NFT marketplace | Marketplace logic is good for surface map and readiness review | Check if active and whether issue/contact path exists |
| 11 | `aristematic/nft-marketplace` | NFT marketplace | Marketplace candidate with larger repo size | Check contracts, tests, deployment docs |
| 12 | `0xSmartCoder/bluxe-nft-marketplace` | NFT marketplace | Marketplace candidate with public code | Check contract controls and project maturity |
| 13 | `404priyanshu/nft-marketplace-v2` | NFT marketplace | Small marketplace candidate | Check if real project vs exercise |
| 14 | `AyushSharma7463/NFT_Project` | NFT project | NFT project candidate | Check whether Solidity contracts are central |

---

## Shortlist priority

Start with these five because they map cleanly to the DLSK value proposition:

1. `ShamratDev/ERC20-Token-Hardhat-Multi-Network`
2. `saurabh0829/merkle-airdrop-dapp`
3. `orien7/uday-erc20-staking`
4. `qryptalabs/qrypta-token`
5. `gonzalolater/NFT-Marketplace-Solidity-Hardhat-NexJS-Web3js-Tailwind`

Reason:

- They cover token, staking, airdrop, and marketplace use cases.
- They should expose owner/admin, deployment, tests, CI, and audit-prep readiness questions.
- They are better first tests than generic one-file ERC20 examples.

---

## Outreach rule for this batch

Do not open public issues claiming vulnerabilities.

Use neutral wording:

> I am testing a lightweight AI-assisted pre-audit launch-readiness workflow on public repos. Your project looks like a possible fit. This is not a formal audit and not a public vulnerability report. If useful, I can share a short readiness note covering owner/admin permissions, contract surface, deployment checklist, tests/CI readiness, and audit-prep questions.

Only send this after the first LinkedIn post is live.
