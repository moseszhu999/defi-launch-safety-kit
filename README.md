# DeFi Launch Safety Kit

A lightweight pre-audit and launch safety review toolkit for DeFi and token projects.

`defi-launch-safety-kit` is a Python CLI tool that scans Solidity source code and generates a launch-readiness risk report. It is designed for small DeFi/token teams, independent reviewers, and builders who want a structured pre-audit checklist before commissioning a formal security audit.

It is **not** a formal audit tool. It does not guarantee that a contract is safe.

## What it checks

The built-in scanner looks for common launch-risk signals:

- Owner/admin/role privileges
- Mint and burn functions
- Pause, blacklist, whitelist, freeze controls
- Tax, fee, router, pair, max transaction, and max wallet logic
- Upgradeability and proxy patterns
- Dangerous Solidity patterns such as `selfdestruct`, `tx.origin`, `delegatecall`, low-level calls, `assembly`, `unchecked`, and emergency withdrawal functions
- Missing launch checklist items, such as tests, deployment scripts, multisig, timelock, vesting policy, liquidity lock policy, and known-risk disclosure

If `slither` is installed locally, the CLI also runs Slither and attaches its output. If Slither is unavailable, the tool automatically falls back to built-in rules.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For development:

```bash
pip install -e .[dev]
```

Optional Slither support:

```bash
pip install -e .[slither]
```

## Quick start

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --out reports/demo
```

Expected output:

```text
Overall Risk: CRITICAL
Findings: ...
Report saved to reports/demo/report.md
```

Generated files:

```text
reports/demo/report.md
reports/demo/report.json
reports/demo/checklist.md
```

## Scan local Solidity source

Scan one Solidity file:

```bash
dlsk scan --source examples/contracts/RiskyToken.sol
```

Scan a directory:

```bash
dlsk scan --source examples/contracts
```

Skip optional Slither integration:

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --no-slither
```

Generate only Markdown:

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --format markdown
```

Generate only JSON:

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --format json
```

## Scan verified chain contracts

The CLI can fetch verified source code from explorer APIs.

```bash
dlsk scan --address 0xContractAddress --chain ethereum
```

Supported chain values:

- `ethereum`
- `bsc`
- `polygon`

## Environment variables

Set explorer API keys when using `--address`:

```bash
ETHERSCAN_API_KEY=
BSCSCAN_API_KEY=
POLYGONSCAN_API_KEY=
```

Copy `.env.example` if needed.

## Audit preparation pack

After running a scan, generate a client-facing audit-prep pack:

```bash
dlsk prep --report reports/demo/report.json --out reports/demo/audit-prep-pack
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

This pack is useful when preparing a small DeFi/token project for a formal audit or external technical review. It organizes scan output into owner/admin permissions, deployment checklist, known-risk disclosure, and questions for the project team.

## Report sections

The Markdown report contains:

1. Summary
2. Key findings
3. Permission risk map
4. Tokenomics / transfer risk
5. Upgradeability risk
6. Dangerous patterns
7. Launch checklist
8. Slither output
9. Disclaimer

## Severity levels

The tool uses five severity levels:

- `INFO`
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

Examples:

- `selfdestruct`: `CRITICAL`
- Privileged mint without obvious cap: `CRITICAL`
- `delegatecall`: `HIGH`
- Blacklist/freeze: `HIGH`
- Upgradeability: `HIGH`
- Adjustable tax/fee: `MEDIUM` to `HIGH`
- Plain `Ownable`: `LOW`
- Checklist gaps: `INFO` or manual-check items

## Example service positioning

This project can support a service offering such as:

- Pre-audit technical review
- DeFi launch safety review
- Token launch checklist review
- Audit preparation pack
- Smart contract risk triage

Avoid calling the output a formal audit. Use it as a structured launch-readiness report.

## Disclaimer

This report is a lightweight pre-audit technical review. It is not a formal security audit and does not guarantee the absence of vulnerabilities. Use it as a launch-readiness checklist and risk triage aid before commissioning a professional audit when funds or users are at risk.

## Roadmap

Implemented through v0.3:

- Etherscan/BscScan/PolygonScan multi-file source parsing
- Owner address EOA vs contract / Safe-like detection
- HTML report export
- Mermaid permission graph
- Audit Preparation Pack generator

Planned v0.4 ideas:

- CI-friendly exit codes by severity
- More precise AST-based analysis
- Foundry/Hardhat coverage extraction
- SARIF export
- Better timelock and Safe module detection
