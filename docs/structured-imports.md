# Structured Imports

DeFi Launch Safety Kit v1.2 can import structured output from compiler and analyzer tools.

Supported inputs:

- solc Standard JSON output / AST-like JSON
- Slither JSON report

This lets the CLI enrich heuristic scan results with compiler-derived contract structure and analyzer-derived findings.

## Import only

```bash
dlsk import-struct \
  --solc-json examples/structured/solc-standard-json-output.json \
  --slither-json examples/structured/slither-report.json \
  --out reports/structured-import
```

Generated files:

```text
reports/structured-import/contract-map.md
reports/structured-import/contract-map.json
reports/structured-import/imported-findings.md
reports/structured-import/imported-findings.json
```

## Use during scan

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

## solc AST import

When solc-derived structure is available, the contract map can be generated from compiler output instead of only regex heuristics.

Imported fields may include:

- contract names
- inheritance hints
- public and external functions
- modifiers
- mutability hints
- state-changing functions
- privileged function surface

## Slither JSON import

Slither detector results are normalized into DLSK findings and included in Markdown, JSON, HTML, and SARIF reports.

Example imported IDs:

```text
SLITHER-CONTROLLED-MINT
SLITHER-ARBITRARY-SEND-ETH
```

## Notes

Structured imports improve the review workflow but do not turn the tool into a formal audit engine. Treat results as pre-audit triage and launch-readiness material.
