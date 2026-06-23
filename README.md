# DeFi Launch Safety Kit

**A lightweight pre-audit and launch-readiness toolkit for DeFi and token projects.**

`defi-launch-safety-kit` helps small DeFi/token teams, independent reviewers, and builders prepare for formal audit or mainnet launch. It scans Solidity projects and generates Markdown, JSON, HTML, and SARIF reports, plus audit-preparation material such as owner/admin permission review, deployment checklist, known-risk notes, project readiness checks, contract surface maps, and structured imports from solc AST / Slither JSON.

> This is **not** a formal security audit and does not guarantee safety. It is defensive launch-readiness triage before commissioning a professional audit when funds or users are at risk.

---

## Who this is for

- Small DeFi/token teams preparing for testnet, mainnet, or formal audit
- Founders who need an early risk checklist before paying for a full audit
- Solidity builders who want CI-friendly launch checks
- Independent reviewers who need a repeatable pre-audit report format
- Teams that need Markdown, HTML, JSON, and SARIF outputs for internal review

## What it checks

- Owner/admin privilege risks
- Mint, burn, pause, blacklist, tax, fee, and transfer-control patterns
- Upgradeability and dangerous Solidity patterns
- ERC20 / staking / vesting / airdrop rule packs
- Contract surface map for public/external and privileged functions
- Foundry / Hardhat project readiness
- Deployment scripts, tests, CI, and coverage-readiness signals
- Structured imports from solc Standard JSON AST and Slither JSON
- SARIF output for GitHub Code Scanning / CI security gates

---

## Quick demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

dlsk scan \
  --source examples/contracts/RiskyToken.sol \
  --profile erc20 \
  --format all \
  --out reports/demo \
  --no-slither
```

Generated files:

```text
reports/demo/report.md
reports/demo/report.json
reports/demo/report.html
reports/demo/report.sarif
reports/demo/checklist.md
```

Optional Slither support:

```bash
pip install -e .[slither]
```

---

## Audit preparation pack

Turn scan results into client/auditor-facing preparation material:

```bash
dlsk prep \
  --report reports/demo/report.json \
  --out reports/demo/audit-prep-pack
```

Generated files:

```text
audit-prep-pack/README.md
audit-prep-pack/audit-prep.md
audit-prep-pack/owner-permissions.md
audit-prep-pack/deployment-checklist.md
audit-prep-pack/known-risks.md
audit-prep-pack/questions-for-team.md
```

---

## Contract surface map

```bash
dlsk map \
  --source examples/contracts/RiskyToken.sol \
  --out reports/contract-map
```

Outputs:

```text
reports/contract-map/contract-map.md
reports/contract-map/contract-map.json
```

The map highlights:

- contracts, interfaces, and libraries
- inheritance hints
- public / external functions
- mutability hints such as view, pure, payable
- modifiers
- public state-changing functions
- privileged functions such as mint, pause, blacklist, rescue, withdraw, upgrade

---

## Structured imports

Import compiler and analyzer outputs:

```bash
dlsk import-struct \
  --solc-json examples/structured/solc-standard-json-output.json \
  --slither-json examples/structured/slither-report.json \
  --out reports/structured-import
```

Use structured inputs during scan:

```bash
dlsk scan \
  --source examples/contracts/RiskyToken.sol \
  --profile erc20 \
  --solc-json examples/structured/solc-standard-json-output.json \
  --slither-json examples/structured/slither-report.json \
  --format all \
  --out reports/demo-v12 \
  --no-slither
```

---

## Policy config

Create a config file:

```bash
dlsk init-config --out dlsk.yml
```

Example:

```yaml
enabled_packs:
  - erc20
  - staking

fail_on: high

severity_overrides:
  DLSK-ERC20-003: MEDIUM

ignore:
  - DLSK-ERC20-002
  - category:Operational Security
```

---

## Baseline diff mode

Create a baseline:

```bash
dlsk baseline create \
  --report reports/main/report.json \
  --out dlsk-baseline.json
```

Block only newly introduced high-risk findings:

```bash
dlsk scan \
  --source contracts \
  --config dlsk.yml \
  --baseline dlsk-baseline.json \
  --fail-on-new high \
  --format all \
  --out reports/ci
```

---

## Project readiness

```bash
dlsk readiness \
  --source examples/projects/foundry-token \
  --out reports/readiness
```

Readiness checks include Foundry/Hardhat detection, tests, deployment scripts, coverage artifacts, CI workflow files, and privileged-flow test hints.

---

## Rule packs

```bash
dlsk rule-packs
```

Supported profiles:

- `erc20`
- `staking`
- `vesting`
- `airdrop`
- `auto`
- `all`

---

## CI / SARIF

```bash
dlsk scan \
  --source contracts \
  --config dlsk.yml \
  --format sarif \
  --fail-on high \
  --out reports/ci
```

SARIF can be uploaded to GitHub Code Scanning from GitHub Actions.

---

## Articles

- [20 Risks to Check Before Launching an ERC20 Token](docs/articles/20-erc20-launch-risks.md)

## Case studies

- [Demo ERC20 Launch-Readiness Review](docs/case-studies/demo-erc20-launch-review.md)

## Request a review

Use the GitHub issue template to request a lightweight launch-readiness review:

- [Request a launch-readiness review](../../issues/new?template=launch-readiness-review.md)

Best-fit projects:

- ERC20 / staking / vesting / airdrop projects before formal audit
- Small teams preparing for testnet or mainnet
- Teams that want a structured pre-audit checklist before spending on a formal audit

---

## Useful docs

- `docs/structured-imports.md`
- `docs/contract-surface-map.md`
- `docs/project-readiness.md`
- `docs/baseline-diff.md`
- `docs/policy-config.md`
- `docs/rule-packs.md`
- `docs/finding-taxonomy.md`
- `docs/launch-review-service-one-pager.md`
- `docs/github-profile-readme-snippet.md`
- `docs/linkedin-launch-post.md`
- `docs/github-marketing-playbook.md`
- `docs/github-profile-readme.md`
- `docs/linkedin-posts/erc20-launch-risks-post.md`
- `docs/linkedin-posts/demo-case-study-post.md`

---

## Need a launch-readiness review?

This project can support services such as:

- Pre-audit technical review
- DeFi/token launch safety review
- Audit preparation pack
- Owner/admin permission review
- GitHub Actions / SARIF security gate setup
- Project readiness review before formal audit

Typical early-stage review scope:

```text
1. Run DLSK scan on the repository
2. Review owner/admin, mint, pause, blacklist, tax, fee, rescue, withdraw, and upgrade paths
3. Generate a Markdown/HTML report
4. Generate an audit-preparation pack
5. Provide a short remediation checklist before formal audit or mainnet launch
```

Contact: open an issue in this repository or reach out via the maintainer profile.

---

## Disclaimer

This project provides lightweight pre-audit technical review and launch-readiness triage. It is not a formal security audit and does not guarantee the absence of vulnerabilities.
