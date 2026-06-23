# DeFi Launch Safety Kit

A lightweight pre-audit and launch-readiness toolkit for DeFi and token projects.

`defi-launch-safety-kit` is a defensive Python CLI for small DeFi/token teams, independent reviewers, and builders preparing for formal audit or mainnet launch.

It scans Solidity projects and generates Markdown, JSON, HTML, and SARIF reports, plus audit-preparation material such as owner/admin permission review, deployment checklist, known-risk notes, project readiness checks, contract surface maps, and structured imports from solc AST / Slither JSON.

> This is **not** a formal security audit. It does not guarantee safety. Use it as launch-readiness triage before commissioning a professional audit when funds or users are at risk.

## Highlights

- Solidity source scanning for common launch-risk signals
- ERC20 / staking / vesting / airdrop rule packs
- Stable finding IDs such as `DLSK-ERC20-006`
- Markdown, JSON, HTML, and SARIF output
- CI gate support with `--fail-on` and `--fail-on-new`
- Baseline diff mode so CI can block only newly introduced risk
- Configurable policy via `dlsk.yml`
- Foundry / Hardhat project readiness checks
- Contract surface map for public/external and privileged functions
- Audit preparation pack generator
- Structured imports from solc Standard JSON AST and Slither JSON

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Optional Slither support:

```bash
pip install -e .[slither]
```

## Quick start

```bash
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

## Audit preparation pack

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

## Project readiness

```bash
dlsk readiness \
  --source examples/projects/foundry-token \
  --out reports/readiness
```

Readiness checks include Foundry/Hardhat detection, tests, deployment scripts, coverage artifacts, CI workflow files, and privileged-flow test hints.

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

## Useful docs

- `docs/structured-imports.md`
- `docs/contract-surface-map.md`
- `docs/project-readiness.md`
- `docs/baseline-diff.md`
- `docs/policy-config.md`
- `docs/rule-packs.md`
- `docs/finding-taxonomy.md`
- `docs/launch-review-service-one-pager.md`

## Service positioning

This project supports services such as:

- Pre-audit technical review
- DeFi/token launch safety review
- Audit preparation pack
- Owner/admin permission review
- GitHub Actions / SARIF security gate setup
- Project readiness review before formal audit

## Disclaimer

This project provides lightweight pre-audit technical review and launch-readiness triage. It is not a formal security audit and does not guarantee the absence of vulnerabilities.
