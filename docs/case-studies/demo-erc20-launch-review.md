# Demo ERC20 Launch-Readiness Review

This is a demo case study showing how `defi-launch-safety-kit` can be used as a lightweight pre-audit and launch-readiness workflow for an ERC20-style token project.

> This case study uses an intentionally risky demo contract. It is not a report on a real project.

---

## Review objective

The goal is not to replace a formal audit. The goal is to help a small team understand obvious launch blockers before paying for a professional audit or deploying to mainnet.

The review focuses on:

- privileged owner/admin functions
- mint, burn, pause, blacklist, fee, and tax controls
- external/public state-changing functions
- dangerous Solidity patterns
- project readiness: tests, deployment scripts, CI, coverage signals
- audit-preparation material for internal and auditor-facing review

---

## Example command

```bash
dlsk scan \
  --source examples/contracts/RiskyToken.sol \
  --profile erc20 \
  --format all \
  --out reports/demo-launch-review \
  --no-slither
```

Optional audit-preparation pack:

```bash
dlsk prep \
  --report reports/demo-launch-review/report.json \
  --out reports/demo-launch-review/audit-prep-pack
```

Optional contract surface map:

```bash
dlsk map \
  --source examples/contracts/RiskyToken.sol \
  --out reports/demo-launch-review/contract-map
```

---

## High-level result

A risky ERC20 launch review should answer four questions quickly:

1. Can the owner mint, pause, blacklist, rescue, withdraw, or change fees?
2. Are those powers clearly documented and protected by multisig/timelock?
3. Are critical flows covered by tests and deployment scripts?
4. Is the project ready for a formal audit handoff?

For the demo contract, the answer is intentionally poor: the contract contains multiple privileged and operational-risk patterns that should be resolved or explicitly documented before launch.

---

## Key findings to investigate

### 1. Owner/admin privilege concentration

A single owner/admin role controlling mint, pause, blacklist, fee, rescue, or withdraw paths is a major launch risk. Even if the owner is honest, a compromised EOA can become a project-wide failure point.

Suggested remediation:

- use a multisig for privileged roles
- document every privileged function
- add timelock where appropriate
- publish an owner/admin operations policy

### 2. Mint authority

A mint function can be legitimate, but unlimited or poorly documented mint authority is a major trust issue for token holders.

Suggested remediation:

- cap supply if the token economics require it
- restrict minting to a documented role
- add event coverage and tests
- disclose mint authority clearly in launch docs

### 3. Pause / blacklist / transfer control

Pause and blacklist controls may be required for compliance or emergency response, but they are also centralization and censorship risks.

Suggested remediation:

- document the exact conditions for use
- restrict execution to multisig/timelock
- add tests for blocked and unblocked flows
- disclose these controls before launch

### 4. Rescue / sweep / emergency withdraw paths

Rescue and sweep functions can prevent funds from getting stuck, but they can also become fund-drain paths when incorrectly scoped.

Suggested remediation:

- restrict what can be rescued
- avoid sweeping core user funds
- emit clear events
- test rescue behavior against representative token balances

### 5. Missing launch-readiness evidence

A project that lacks test files, deployment scripts, CI, coverage signals, and known-risk documentation is not ready for serious audit handoff.

Suggested remediation:

- add Foundry or Hardhat tests
- test privileged flows explicitly
- add deterministic deployment scripts
- run CI on pull requests
- generate an audit-preparation pack

---

## Deliverables for a lightweight review

A useful launch-readiness review should produce:

- Markdown report for human review
- JSON report for automation
- HTML report for sharing
- SARIF report for CI/code-scanning integration
- contract surface map
- owner/admin permission review
- deployment checklist
- known-risk notes
- questions for the project team

---

## What this is not

This workflow does not replace:

- formal smart contract audit
- economic/game-theoretic review
- protocol design review
- legal/compliance review
- incident-response planning

It is an early triage layer that helps a small team avoid entering formal audit or mainnet launch with obvious gaps.

---

## Next step

If this were a real project, the next step would be to turn the findings into an issue-based remediation plan:

1. remove or constrain dangerous privileged functions
2. move admin ownership to multisig/timelock
3. document known risks
4. add missing tests and deployment scripts
5. rerun the scan and compare against a baseline
