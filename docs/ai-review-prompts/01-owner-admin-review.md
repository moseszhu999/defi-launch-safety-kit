# AI Review Prompt: Owner/Admin Permission Review

You are reviewing a Solidity project before formal audit or mainnet launch.

Goal: identify owner/admin powers that need documentation, governance controls, or manual review.

Inputs to paste below:

- Solidity contracts
- DLSK `report.json` or `report.md`
- Contract surface map, if available
- Deployment assumptions, if available

## Review checklist

1. List every owner/admin/role-controlled function.
2. Identify mint, burn, pause, blacklist, whitelist, fee/tax, rescue, withdraw, upgrade, oracle, router, and treasury powers.
3. Explain who can call each privileged path.
4. Identify whether the privileged caller is likely to be an EOA, multisig, timelock, DAO, or unknown.
5. Flag any role that could change user balances, transfer rules, supply, treasury funds, implementation, or trading behavior.
6. Separate launch blockers from documentation items.
7. Do not claim this is a formal audit.

## Output format

- Summary
- Privileged function table
- Launch blockers
- Documentation gaps
- Questions for the team
- Recommended next actions
