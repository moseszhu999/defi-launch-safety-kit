# AI-Assisted Launch-Readiness Workflow

Large language models can already review Solidity code, explain suspicious patterns, and help teams reason about launch risk.

That changes the role of this project.

DeFi Launch Safety Kit should not be positioned as another standalone Solidity scanner or an AI auditor. Its stronger role is to help small DeFi/token teams turn scans, AI review notes, owner/admin checks, contract surface maps, deployment checklists, and audit-preparation notes into a reproducible launch-readiness evidence pack.

## Positioning

Use this positioning:

> DeFi Launch Safety Kit is an AI-assisted pre-audit launch-readiness workflow for small DeFi and token teams.

Avoid these claims:

- automated audit replacement
- AI smart contract auditor
- finds all vulnerabilities
- guarantees safety
- formal audit alternative

Prefer these claims:

- pre-audit launch-readiness workflow
- audit-preparation evidence pack
- owner/admin permission review
- human-in-the-loop AI review prompts
- baseline diff for newly introduced risk
- GitHub-native security gate
- structured handoff before formal audit

## Why this still matters in the AI era

A team can ask an AI model to review Solidity code, but raw AI output is not enough for launch readiness.

The missing layer is evidence discipline:

- What code was scanned?
- What privileged functions exist?
- Which findings are confirmed, ignored, or accepted?
- Which issues are launch blockers?
- Which items only need disclosure?
- What should be handed to a formal auditor?
- What changed since the last baseline?
- What did the team actually decide?

DLSK should organize this evidence so a founder, developer, investor, launchpad, community member, or auditor can inspect it later.

## Recommended workflow

```text
1. Run static / heuristic scan.
2. Generate Markdown, JSON, HTML, and SARIF outputs.
3. Generate contract surface map.
4. Generate audit-preparation pack.
5. Generate AI review prompt pack.
6. Use AI to review one narrow question at a time.
7. Human reviewer confirms or rejects AI notes.
8. Finalize launch-readiness evidence pack.
9. Use baseline diff in CI to detect newly introduced risks.
10. Hand confirmed materials to the team or formal auditor.
```

## Example command flow

```bash
dlsk scan \
  --source contracts \
  --format all \
  --out reports/latest

# If available in the project version:
dlsk map \
  --source contracts \
  --out reports/latest/contract-map

# Generate AI prompt pack:
dlsk ai-pack \
  --out reports/latest/ai-review-prompts
```

Then paste each prompt into an AI model together with the relevant evidence:

- `report.md` or `report.json`
- `checklist.md`
- contract surface map
- deployment scripts
- README / docs
- known-risk notes
- selected Solidity source excerpts

## Prompt pack structure

```text
ai-review-prompts/
  README.md
  01-owner-admin-review.md
  02-tokenomics-risk-review.md
  03-upgradeability-review.md
  04-launch-blocker-review.md
  05-audit-prep-summary.md
```

## Human-in-the-loop rule

AI output should be treated as review input, not proof of safety.

Every AI-generated item should be classified as:

- `CONFIRMED`
- `NEEDS_TEAM_CONFIRMATION`
- `FALSE_POSITIVE`
- `DOCUMENTATION_GAP`
- `ACCEPTED_RISK`
- `LAUNCH_BLOCKER`

Only confirmed or explicitly accepted items should appear in the final evidence pack.

## Service framing

This workflow supports services such as:

- quick launch-readiness review
- owner/admin permission review
- audit-preparation pack
- AI-assisted Solidity review workflow setup
- GitHub Actions / SARIF security gate setup
- pre-audit evidence pack for small token teams

Do not sell it as a formal audit.

Sell it as the layer before formal audit: the part that makes a small team organized, honest, and ready.
