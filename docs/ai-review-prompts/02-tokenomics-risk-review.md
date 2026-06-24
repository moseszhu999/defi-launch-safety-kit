# AI Review Prompt: Tokenomics and Transfer-Risk Review

You are reviewing an ERC20/token project before launch.

Goal: identify tokenomics-related implementation risks that should be disclosed or checked before audit/mainnet.

Inputs to paste below:

- Solidity contracts
- Tokenomics notes
- DLSK findings
- Deployment checklist

## Review checklist

1. Detect supply cap, mint policy, burn policy, decimals, initial distribution, vesting, airdrop, tax/fee, blacklist/whitelist, max wallet, max transaction, anti-bot, and DEX/router behavior.
2. Identify mutable tokenomics parameters and who can change them.
3. Explain whether any mechanism could surprise users after launch.
4. Identify documentation gaps rather than making unsupported accusations.
5. Separate hard risks from normal launch-policy choices.

## Output format

- Token behavior summary
- Mutable parameters
- User-impacting powers
- Disclosure gaps
- Launch blockers
- Questions for the team
