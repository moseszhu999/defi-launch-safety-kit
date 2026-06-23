# DeFi Launch Safety Kit

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-v0.1_MVP-orange)

A lightweight pre-audit and launch safety review toolkit for DeFi and token projects.

This project is a defensive CLI tool for small crypto teams, technical consultants, and builders who want a quick launch-safety review before a formal audit. It scans Solidity source code for common launch risks such as privileged owner functions, mint/burn authority, blacklist/freeze mechanisms, mutable taxes/fees, upgradeability, low-level calls, rescue/withdraw functions, and missing launch checklist items.

It is **not** a formal security audit tool. It does **not** guarantee safety. It is designed to help teams prepare for audit, improve documentation, and discover obvious pre-launch risk areas.

## Features

- Local Solidity source scanning
- Optional verified-source fetching from Etherscan-style APIs
- Built-in heuristic scanner for common launch risks
- Optional Slither integration when installed locally
- Markdown and JSON report generation
- Launch checklist generation
- Demo contracts for safe/risky/upgradeable examples

## Installation

```bash
cd defi-launch-safety-kit
python -m pip install -e .
```

For development:

```bash
python -m pip install -e .[dev]
```

Optional Slither support:

```bash
python -m pip install slither-analyzer
```

## Quick Start

Scan a local contract:

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --out reports/demo
```

Expected output:

```text
Overall Risk: CRITICAL or HIGH
Findings: ...
Markdown report saved to: reports/demo/report.md
JSON report saved to: reports/demo/report.json
```

Generated files:

```text
reports/demo/report.md
reports/demo/report.json
reports/demo/checklist.md
```

## Scan Local Source

```bash
dlsk scan --source examples/contracts/RiskyToken.sol
```

```bash
dlsk scan --source examples/contracts
```

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --format markdown
```

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --format json
```

```bash
dlsk scan --source examples/contracts/RiskyToken.sol --no-slither
```

## Scan Verified Chain Contracts

Set explorer API keys:

```bash
export ETHERSCAN_API_KEY=your_key
export BSCSCAN_API_KEY=your_key
export POLYGONSCAN_API_KEY=your_key
```

Then run:

```bash
dlsk scan --address 0x0000000000000000000000000000000000000000 --chain ethereum
```

Supported chain options:

- `ethereum`
- `bsc`
- `polygon`

If the API key is missing or the contract is not verified, the CLI prints a friendly error.

## Environment Variables

Copy `.env.example` and fill keys if you want source fetching:

```text
ETHERSCAN_API_KEY=
BSCSCAN_API_KEY=
POLYGONSCAN_API_KEY=
```

The CLI does not require these keys for local source scanning.

## Risk Rules

The built-in scanner highlights these categories:

- Permissions: Ownable, owner, onlyOwner, AccessControl, admin roles
- Mint/Burn: mint, _mint, burn, _burn, supply-cap signals
- Pause/Blacklist: pause, unpause, blacklist, freeze, allowlist
- Tax/Fee/Transfer Hooks: tax, fee, setTax, setFee, maxTx, maxWallet
- Upgrade/Proxy: UUPS, Initializable, upgradeTo, delegatecall, proxy
- Dangerous Patterns: selfdestruct, tx.origin, call, assembly, emergency withdraws

## Output Report

The Markdown report contains:

1. Summary
2. Key Findings
3. Permission Risk Map
4. Tokenomics / Transfer Risk
5. Upgradeability Risk
6. Dangerous Patterns
7. Launch Checklist
8. Slither Notes
9. Disclaimer

The JSON report is machine-readable and can be used by future dashboards or SaaS versions.

## Testing

```bash
pytest
```

## Intended Use Cases

- Pre-audit technical review
- Launch checklist preparation
- Internal technical due diligence
- Audit preparation pack
- Small project risk triage
- Portfolio demo for crypto security/backend consulting

## Disclaimer

This report is a lightweight pre-audit technical review. It is not a formal security audit and does not guarantee the absence of vulnerabilities.

The built-in scanner is heuristic. It may produce false positives and false negatives. Production crypto systems should still receive professional security review, comprehensive testing, deployment verification, operational monitoring, and legal/compliance review where applicable.

## Roadmap

- v0.2: Better Etherscan/BscScan/PolygonScan multi-file source handling
- v0.2: Detect whether owner/admin is EOA, contract, or Safe multisig
- v0.2: Foundry/Hardhat test coverage summary
- v0.3: Permission graph visualization
- v0.3: Treasury and privileged event monitor
- v0.4: HTML report export
- v0.5: Optional SaaS dashboard
