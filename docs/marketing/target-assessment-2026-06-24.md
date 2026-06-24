# Target Assessment — 2026-06-24

This note records the first manual assessment after the Day 1 LinkedIn launch.

Goal: filter the first five candidates before any outreach. Do not contact projects until a repo has been checked for credibility, public Solidity code, contact path, and a useful launch-readiness angle.

---

## Summary ranking

| Rank | Repository | Verdict | Why |
|---|---|---|---|
| 1 | `orien7/uday-erc20-staking` | Best first outreach candidate; readiness note drafted | Clear staking/token scope, readable README, explicit author/contact, meaningful owner/mint/reward/lock/penalty surface, Hardhat scripts and tests. Friendly note drafted at `docs/marketing/readiness-notes/orien7-uday-erc20-staking.md`. |
| 2 | `saurabh0829/merkle-airdrop-dapp` | Good candidate, verify contract path first | Strong README, live demo, airdrop/admin/Merkle/security angle. But root package looks frontend-only and contract path was not immediately found. |
| 3 | `qryptalabs/qrypta-token` | Interesting but needs deeper verification | Strong positioning and Hardhat dependencies, but README is short and contract file path was not immediately found. |
| 4 | `ShamratDev/ERC20-Token-Hardhat-Multi-Network` | Good friendly documentation/CI candidate | Simple ERC20 with multi-network README, OpenZeppelin, tests, deployment notes. But package test script does not match README claims. |
| 5 | `gonzalolater/NFT-Marketplace-Solidity-Hardhat-NexJS-Web3js-Tailwind` | Deprioritize | README says tutorial and explicitly says code should not be used in production. Use only as demo/reference, not serious outreach. |

---

## 1. `orien7/uday-erc20-staking`

### Fit

High.

The README presents the project as a production-grade ERC20 token plus staking rewards system. It includes an author identity and external contact links, which makes it better for targeted outreach than anonymous toy repos.

### Useful readiness surface

- ERC20 token with capped supply
- `Ownable2Step`
- owner mint function up to max supply
- staking contract with reward rate, lock period, emergency penalty, minimum stake
- owner functions for reward rate, lock period, and reward funding
- Hardhat compile/test/deploy scripts
- explicit security policy and pre-mainnet requirements

### Verified public-repo evidence

- README includes a Sepolia/mainnet go-live checklist, including audit, multisig owner, Defender, and bug bounty items.
- `UDAYToken.sol` includes owner-controlled `mint` up to max supply.
- `StakingRewards.sol` includes `setRewardRate`, `setLockPeriod`, and `fundRewards` as owner functions.
- Deployment script funds the staking contract with 500,000 UDAY reward tokens.
- Tests cover staking, rewards, unstaking, and emergency withdraw user flows.
- Security policy asks not to open public vulnerability issues, so outreach should be friendly/documentation-focused or via LinkedIn.

### Draft readiness note

Created:

- `docs/marketing/readiness-notes/orien7-uday-erc20-staking.md`

### Suggested note angle

Do not frame this as vulnerability reporting.

Frame it as:

> Your staking project is a good fit for a launch-readiness evidence pack because it has owner-controlled reward parameters, mint authority, lock/penalty assumptions, and reward funding assumptions that are worth documenting before audit or testnet feedback.

### First observations

- Document owner-controlled `mint`, `setRewardRate`, `setLockPeriod`, and `fundRewards`.
- Make reward solvency assumptions explicit.
- Add tests for owner parameter changes, reward-funding edge cases, and repeated/partial staking semantics.

### Outreach priority

High.

Preferred contact path: LinkedIn first. Do not open a public security issue.

---

## 2. `saurabh0829/merkle-airdrop-dapp`

### Fit

Medium-high, pending contract verification.

The README is polished and includes a live demo. It claims a full-stack Web3 airdrop platform with Merkle proofs, admin panel, Solidity, OpenZeppelin, Hardhat, Next.js, wagmi, and viem.

### Useful readiness surface

- Merkle root update process
- admin CSV upload and root generation
- claim authorization and proof binding
- double-claim prevention
- token pause/burn/ownable assumptions
- frontend/admin trust boundary

### Concern

The root `package.json` looked frontend-only during quick inspection. The usual contract paths were not immediately found. Before outreach, verify whether Solidity contracts are actually public in the repo.

### Suggested note angle

> Your Merkle airdrop dApp looks like a strong fit for an AI-assisted launch-readiness pass, especially around root update authority, admin workflow, proof binding, double-claim assumptions, and deployment documentation.

### Outreach priority

Medium-high after contract path is verified.

---

## 3. `qryptalabs/qrypta-token`

### Fit

Medium, pending deeper verification.

The README positions Qrypta as post-quantum value transfer infrastructure with ZK verification on BNB Smart Chain and Ethereum. The package uses Hardhat and OpenZeppelin.

### Useful readiness surface

Potentially strong if contracts are present:

- token launch assumptions
- ownership/admin privileges
- ZK verification claims
- deployment readiness
- Ethereum / BNB Chain dual-chain documentation

### Concern

README is short and a likely contract filename was not immediately found. Before outreach, inspect the repository tree manually or clone locally.

### Suggested note angle

> The project positioning is ambitious. A launch-readiness evidence pack could help clarify what is implemented in Solidity today, what is roadmap/architecture, and which admin/security assumptions should be documented before wider release.

### Outreach priority

Medium. Verify code first.

---

## 4. `ShamratDev/ERC20-Token-Hardhat-Multi-Network`

### Fit

Medium.

The README says the token is fully tested, fixed-supply, OpenZeppelin-based, and supports multi-network deployment. The contract itself is a simple fixed-supply ERC20 using `Ownable`.

### Useful readiness surface

- fixed-supply documentation
- ownership notes
- multi-network deployment checklist
- `.env` and private key handling
- test script / README consistency
- verification checklist

### Concern

The root `package.json` test script says `Error: no test specified`, while the README points to Mocha/Chai tests. This is a useful friendly documentation/CI-readiness finding rather than a security issue.

### Suggested note angle

> This repo is a good fit for a lightweight launch-readiness note focused on documentation/CI consistency, deployment checklist, private key handling, and owner/fixed-supply explanation.

### Outreach priority

Medium. Good low-risk first public issue if issues are open.

---

## 5. `gonzalolater/NFT-Marketplace-Solidity-Hardhat-NexJS-Web3js-Tailwind`

### Fit

Low for serious outreach.

The README explicitly identifies the repo as a tutorial and says the code should not be used in production.

### Suggested use

Do not contact as a serious launch-readiness target.

Use only as:

- demo scan input
- tutorial-style example
- comparison case for why production readiness differs from tutorial code

### Outreach priority

Low / skip.

---

## Next action

1. Optionally send the soft LinkedIn message for `orien7/uday-erc20-staking`.
2. Verify contract paths for `saurabh0829/merkle-airdrop-dapp`.
3. Verify code structure for `qryptalabs/qrypta-token`.
4. Prepare one low-risk public documentation/CI note for `ShamratDev/ERC20-Token-Hardhat-Multi-Network`.

Recommended first outreach:

> `orien7/uday-erc20-staking` via LinkedIn, using a soft ask before sharing the full note.
