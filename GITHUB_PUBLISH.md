# Publish Notes

This repository was initialized as a public portfolio project for crypto launch-safety work.

## Suggested repository description

A lightweight pre-audit and launch safety review toolkit for DeFi and token projects.

## Suggested topics

`defi`, `solidity`, `smart-contracts`, `pre-audit`, `token-launch`, `security`, `slither`, `web3`

## Local check

```bash
python -m pip install -e .[dev]
pytest
dlsk scan --source examples/contracts/RiskyToken.sol --out reports/demo --no-slither
```
