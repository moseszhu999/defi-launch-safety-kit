# 20 Risks to Check Before Launching an ERC20 Token

Launching an ERC20 token is not only a Solidity deployment task. It is a launch-readiness problem.

Small token teams often focus on the token name, symbol, supply, listing plan, and community announcement. But many launch failures come from basic engineering and governance risks: excessive owner privileges, unsafe mint controls, missing deployment records, untested pause flows, unclear upgrade authority, and no audit-preparation materials.

This article is a practical checklist for builders preparing an ERC20 token for testnet, audit, or mainnet launch.

> Disclaimer: This is not a formal security audit and not financial advice. It is a pre-audit and launch-readiness checklist.

---

## 1. Unbounded mint authority

If the owner or admin can mint unlimited tokens, the project has a major trust and governance risk.

Check:

- Who can call `mint`?
- Is there a cap?
- Is minting permanently disabled after launch?
- Is mint authority controlled by a multisig or a single EOA?

---

## 2. Owner-controlled burn logic

Burn functions can be legitimate, but dangerous if an owner can burn user balances or supply without clear rules.

Check:

- Can users burn only their own tokens?
- Can an admin burn another account's tokens?
- Is this disclosed in the documentation?

---

## 3. Pause and unpause authority

Pausable tokens are common, but pause authority is a strong centralized control.

Check:

- Who can pause transfers?
- Who can unpause?
- Is pause authority temporary or permanent?
- Are pause flows tested?

---

## 4. Blacklist or blocklist logic

Blacklist features may be required for compliance, but they also introduce censorship risk and governance responsibility.

Check:

- Who can blacklist an address?
- Can blacklisted users recover funds?
- Is this behavior disclosed to users?

---

## 5. Transfer tax or fee controls

Fee-on-transfer tokens often include owner-controlled tax parameters. These can become serious launch risks if fees can be changed after launch.

Check:

- Can the owner change tax rates?
- Is there a maximum fee?
- Can fees be set to 100%?
- Where do collected fees go?

---

## 6. Hidden transfer hooks

Custom `_transfer`, `_beforeTokenTransfer`, or `_afterTokenTransfer` logic can hide restrictions, taxes, blacklists, or balance changes.

Check:

- Are transfer hooks simple and documented?
- Do they call external contracts?
- Do they alter balances unexpectedly?

---

## 7. Single EOA owner

A single externally owned account controlling owner/admin powers is operationally fragile.

Check:

- Is the owner a single wallet?
- Is ownership transferred to a multisig before launch?
- Is there a documented key-management plan?

---

## 8. Missing ownership transfer plan

Many teams deploy with a temporary deployer wallet and forget to transfer ownership.

Check:

- Who is the initial owner?
- When will ownership be transferred?
- Is the target owner address documented?

---

## 9. Upgradeable proxy risk

Upgradeable contracts add flexibility, but also add governance and implementation risks.

Check:

- Is the contract upgradeable?
- Who controls upgrades?
- Is the implementation verified?
- Is there a timelock or multisig?

---

## 10. Rescue or sweep functions

`rescueTokens`, `sweep`, `withdraw`, and similar functions can be useful for stuck funds, but they can also move assets unexpectedly.

Check:

- What assets can be rescued?
- Can the owner rescue the token itself?
- Are rescue functions restricted and documented?

---

## 11. Emergency withdrawal logic

Emergency withdrawal is common in staking or reward systems, but it can become a privileged fund movement path.

Check:

- Who can trigger emergency withdrawal?
- Where do funds go?
- Is user accounting preserved?

---

## 12. `tx.origin` usage

Using `tx.origin` for authorization is dangerous and should generally be avoided.

Check:

- Does the contract use `tx.origin`?
- Is authorization based on `msg.sender` instead?

---

## 13. Low-level calls

Low-level `call`, `delegatecall`, and assembly can be necessary in advanced systems, but they increase audit complexity.

Check:

- Are low-level calls necessary?
- Are return values checked?
- Is reentrancy considered?

---

## 14. Timestamp-dependent behavior

Block timestamps can be manipulated within limits and should not be used as a source of randomness.

Check:

- Does token behavior depend on `block.timestamp`?
- Is timestamp logic used for vesting, fees, or launch windows?

---

## 15. Permit / approval edge cases

Permit and allowance logic are common sources of integration and user-safety issues.

Check:

- Is `permit` implemented correctly?
- Are nonces handled correctly?
- Are approval race conditions considered?

---

## 16. Missing Foundry or Hardhat tests

A token launch without automated tests is not ready for audit or mainnet.

Check tests for:

- Minting
- Burning
- Pausing
- Ownership transfer
- Fee logic
- Blacklist logic
- Upgrade or rescue paths

---

## 17. No deployment script

Manual deployment increases the risk of misconfiguration and missing records.

Check:

- Is deployment scripted?
- Are constructor parameters documented?
- Are deployed addresses recorded?

---

## 18. No CI security gate

For public repositories, GitHub Actions can prevent new high-risk changes from entering the main branch.

Check:

- Does CI run tests?
- Does CI run static analysis?
- Does CI produce SARIF or machine-readable results?

---

## 19. No audit-preparation pack

Auditors need context. A clean audit-preparation pack can reduce confusion and review time.

Prepare:

- Contract list
- Owner/admin permissions
- Deployment checklist
- Known risks
- External dependencies
- Questions for the team

---

## 20. No clear disclaimer to users

If a token has owner controls, blacklist logic, taxes, upgradeability, or emergency functions, users should not discover them only after launch.

Check:

- Are privileged controls disclosed?
- Are admin addresses public?
- Is upgradeability explained?
- Are risk tradeoffs documented?

---

## A lightweight way to start

I built **DeFi Launch Safety Kit** as a lightweight pre-audit and launch-readiness toolkit for DeFi/token projects.

It can generate:

- Markdown, JSON, HTML, and SARIF reports
- Owner/admin permission review
- Contract surface map
- Launch checklist
- Audit-preparation pack
- Foundry/Hardhat project-readiness checks
- Baseline diff mode for CI
- solc AST / Slither JSON structured imports

Repository:

https://github.com/moseszhu999/defi-launch-safety-kit

This does not replace a formal audit. It helps small teams prepare better before audit or mainnet launch.
