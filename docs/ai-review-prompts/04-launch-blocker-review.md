# AI Review Prompt: Launch-Blocker Review

You are reviewing a Solidity project immediately before testnet, mainnet, or formal audit.

Goal: produce a short launch-readiness triage, not a full audit.

Inputs to paste below:

- DLSK `report.md` or `report.json`
- DLSK `checklist.md`
- Contract surface map
- Project README
- Deployment assumptions

Classify each issue as:

- `BLOCKER`: should be fixed or explicitly accepted before mainnet.
- `NEEDS_TEAM_CONFIRMATION`: cannot decide without project context.
- `DOCUMENTATION_GAP`: should be disclosed in audit-prep materials.
- `LOW_PRIORITY`: can wait.

## Review checklist

1. Privileged functions.
2. Upgradeability.
3. Mint/burn/supply.
4. Pausing/freezing/blacklisting.
5. Mutable tax/fee/transfer rules.
6. Treasury/rescue/withdraw powers.
7. Deployment scripts and owner transfer.
8. Test coverage around privileged flows.
9. Known-risk notes.
10. Audit-prep questions.

## Output format

- Executive summary
- Blockers
- Needs confirmation
- Documentation gaps
- Suggested GitHub issue text
- Suggested auditor handoff notes
