# Friendly Readiness Note Draft — Lrvoron/bomtok-erc20

Target repository:

- `Lrvoron/bomtok-erc20`
- Public repo: yes
- Type: ERC20 portfolio project
- Outreach risk: low
- Suggested status: good first feedback target

This is not a formal audit and should not be presented as a vulnerability report.

Use it as a low-pressure example to ask whether this kind of launch-readiness note format is useful for builders.

---

## Why this is a good first target

The project is explicitly described as a production-style ERC20 portfolio project using Hardhat 3, Solidity, TypeScript, Mocha, Ethers v6, and OpenZeppelin Contracts.

The README is clear and includes:

- token name/symbol
- Sepolia deployment address
- explorer link
- owner-only mint
- cap
- burn support
- pause/unpause support
- two-step ownership transfer
- tests
- deploy script
- verification command

That makes it easier to give useful feedback without sounding like a security accusation.

---

## Observed readiness surface

From the README and contract:

- fixed max supply: `1,000,000 BMT`
- owner-only `mint`
- owner-only `pause`
- owner-only `unpause`
- burn support through `ERC20Burnable`
- two-step ownership transfer through `Ownable2Step`
- Sepolia deployment and verification flow
- test coverage for name/symbol, owner mint, non-owner mint rejection, cap, pause/unpause, transfer while paused, burn, and ownership transfer

---

## Friendly note idea

### 1. Add an owner/admin permission table

The README already lists owner-only mint and pause/unpause.

A useful launch-readiness improvement would be to add a compact table:

| Function | Who can call | Launch implication | Suggested production control |
|---|---|---|---|
| `mint(to, amount)` | owner | Can increase supply up to cap | multisig or documented owner wallet |
| `pause()` | owner | Can stop token transfers | incident response policy |
| `unpause()` | owner | Can resume transfers | multisig or documented procedure |
| `transferOwnership` / `acceptOwnership` | owner / new owner | Changes admin control | two-step transfer record |

This is not a code change. It is launch-readiness documentation.

### 2. Document the intended post-deployment owner model

The contract uses `Ownable2Step`, which is a strong signal.

For readiness, the project could document:

- who the Sepolia owner is
- whether mainnet owner would be EOA, multisig, or timelock
- whether minting remains active after launch
- whether pause is intended only for emergency response
- whether ownership will be transferred after deployment

This makes the project easier for reviewers, users, or auditors to understand.

### 3. Add a short launch checklist section

The README already has setup, deploy, verify, and test sections.

A small checklist could make it more complete:

- [ ] deployer wallet separated from owner wallet
- [ ] owner address confirmed before deploy
- [ ] contract verified on explorer
- [ ] max supply documented
- [ ] mint plan documented
- [ ] pause/unpause policy documented
- [ ] ownership transfer tested on testnet
- [ ] `.env` not committed
- [ ] final test run recorded before deploy

This fits the DLSK positioning better than trying to report vulnerabilities.

---

## Suggested outreach message

```text
Hi — I found your BomTok ERC20 portfolio project while testing a small AI-assisted pre-audit launch-readiness note format for public Solidity repos.

I am not reaching out as an auditor, and this is not a vulnerability report.

Your repo looked like a good low-pressure example because the README is clear, the token has owner-only mint/pause controls, Sepolia deployment info, tests, and verification steps.

I drafted a short example note focused on documentation/readiness items such as owner/admin permission table, post-deployment owner model, and launch checklist.

Would you be open to brief feedback on whether this kind of note format is useful for builders?

Project I am testing:
https://github.com/moseszhu999/defi-launch-safety-kit
```

---

## Decision

This is a better first outreach target than the senior UDAY profile.

Recommended action:

1. Send the soft feedback message to the repo owner if a contact path is available.
2. If no contact path is available, open a very neutral GitHub issue only if issues are enabled.
3. Do not mention vulnerabilities.
4. Ask only for feedback on the format.
