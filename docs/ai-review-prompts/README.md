# AI Review Prompt Pack

This prompt pack helps turn DeFi Launch Safety Kit output into a human-reviewed launch-readiness evidence pack.

Use these prompts with your preferred AI model together with:

- `report.md` or `report.json`
- `checklist.md`
- contract surface map
- deployment scripts and assumptions
- known-risk notes
- selected Solidity source excerpts

Important: AI output is review input, not proof of safety. This pack is not a formal security audit.

## Prompts

- [Owner/Admin Permission Review](01-owner-admin-review.md)
- [Tokenomics and Transfer-Risk Review](02-tokenomics-risk-review.md)
- [Upgradeability and Proxy Review](03-upgradeability-review.md)
- [Launch-Blocker Review](04-launch-blocker-review.md)
- [Audit-Preparation Summary](05-audit-prep-summary.md)

## Suggested workflow

1. Run `dlsk scan --format all`.
2. Generate or prepare a contract surface map.
3. Generate an audit-preparation pack if available.
4. Use one prompt at a time with the relevant evidence.
5. Classify each AI-generated note as confirmed, false positive, documentation gap, accepted risk, or launch blocker.
6. Keep only reviewed, confirmed items in the final launch-readiness evidence pack.
