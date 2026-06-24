from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="DeFi / token launch safety review CLI")
console = Console()

SEVERITY_ORDER = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


@dataclass
class Finding:
    severity: str
    category: str
    title: str
    evidence: str
    recommendation: str
    file: str | None = None
    line: int | None = None
    detector: str = "built-in"


@dataclass
class ChecklistItem:
    item: str
    status: str
    recommendation: str


RULES: list[tuple[str, str, str, str, str]] = [
    ("LOW", "Permissions", "Ownable/owner pattern detected", r"\b(Ownable|owner\s*\(|owner\b)\b", "Confirm owner is multisig/timelock or transferred before launch."),
    ("MEDIUM", "Permissions", "onlyOwner-protected function detected", r"\bonlyOwner\b", "Review every owner-only function and document operational controls."),
    ("MEDIUM", "Permissions", "AccessControl admin role detected", r"\b(DEFAULT_ADMIN_ROLE|grantRole|revokeRole|hasRole)\b", "Confirm role admin is not a single EOA and role changes are governed."),
    ("HIGH", "Mint/Burn", "Mint capability detected", r"\b(_mint|mint)\s*\(", "Verify supply cap, mint authority, and post-launch mint policy."),
    ("MEDIUM", "Mint/Burn", "Burn capability detected", r"\b(_burn|burn)\s*\(", "Confirm who can burn tokens and whether user balances can be affected."),
    ("HIGH", "Pause/Freeze", "Pause capability detected", r"\b(Pausable|pause\s*\(|unpause\s*\(|paused)\b", "Document who can pause transfers and under what conditions."),
    ("HIGH", "Pause/Freeze", "Blacklist/freeze capability detected", r"\b(blacklist|BlackList|blocklist|freeze|frozen|isBlacklisted)\b", "Disclose address-freeze powers and governance controls to users."),
    ("MEDIUM", "Pause/Freeze", "Whitelist/allowlist capability detected", r"\b(whitelist|allowlist|isWhitelisted|isAllowed)\b", "Confirm centralized transfer permissions are intentional and documented."),
    ("HIGH", "Tax/Fee", "Mutable tax/fee logic detected", r"\b(tax|fee|buyFee|sellFee|transferFee|setTax|setFee|excludeFromFee|includeInFee)\b", "Review maximum fees, owner controls, and DEX trading impact."),
    ("MEDIUM", "DEX/Trading", "DEX/router/pair control detected", r"\b(setRouter|setPair|router|pair|uniswap|pancake)\b", "Verify router/pair changes cannot be abused after launch."),
    ("MEDIUM", "Transfer Hook", "Transfer hook or transfer override detected", r"\b(_transfer|beforeTokenTransfer|afterTokenTransfer)\b", "Manually review transfer restrictions and side effects."),
    ("HIGH", "Upgradeability", "Upgradeable/proxy pattern detected", r"\b(UUPSUpgradeable|TransparentUpgradeableProxy|upgradeTo|upgradeToAndCall|_authorizeUpgrade|implementation|proxy)\b", "Use multisig/timelock for upgrades and document upgrade policy."),
    ("MEDIUM", "Upgradeability", "Initializer pattern detected", r"\b(Initializable|initializer|reinitializer)\b", "Check initialization cannot be repeated or left uninitialized."),
    ("CRITICAL", "Dangerous Patterns", "selfdestruct detected", r"\bselfdestruct\b", "Remove or formally justify selfdestruct behavior before launch."),
    ("HIGH", "Dangerous Patterns", "delegatecall detected", r"\bdelegatecall\b", "Manually review delegatecall target control and storage safety."),
    ("HIGH", "Dangerous Patterns", "tx.origin authorization risk detected", r"\btx\.origin\b", "Avoid tx.origin for authorization."),
    ("MEDIUM", "Dangerous Patterns", "Low-level call detected", r"\.call\s*(\{|\()", "Review external calls, return values, and reentrancy protections."),
    ("MEDIUM", "Dangerous Patterns", "assembly/unchecked detected", r"\b(assembly|unchecked)\b", "Manually review low-level code and arithmetic assumptions."),
    ("MEDIUM", "Treasury/Rescue", "Emergency/rescue/withdraw function detected", r"\b(emergencyWithdraw|rescueTokens|sweep|withdraw|drain)\b", "Document treasury powers and protect them with multisig."),
    ("LOW", "Signatures", "Signature/permit pattern detected", r"\b(ecrecover|permit)\b", "Review replay protection, domain separator, and nonce logic."),
    ("LOW", "Token Allowance", "Allowance function detected", r"\b(approve|transferFrom)\b", "Confirm allowance behavior follows expected token standard."),
]

AI_REVIEW_PROMPTS: dict[str, str] = {
    "01-owner-admin-review.md": """# AI Review Prompt: Owner/Admin Permission Review

You are reviewing a Solidity project before formal audit or mainnet launch.

Goal: identify owner/admin powers that need documentation, governance controls, or manual review.

Inputs to paste below:
- Solidity contracts
- DLSK report.json or report.md
- Contract surface map, if available
- Deployment assumptions, if available

Review checklist:
1. List every owner/admin/role-controlled function.
2. Identify mint, burn, pause, blacklist, whitelist, fee/tax, rescue, withdraw, upgrade, oracle, router, and treasury powers.
3. Explain who can call each privileged path.
4. Identify whether the privileged caller is likely to be an EOA, multisig, timelock, DAO, or unknown.
5. Flag any role that could change user balances, transfer rules, supply, treasury funds, implementation, or trading behavior.
6. Separate launch blockers from documentation items.
7. Do not claim this is a formal audit.

Output format:
- Summary
- Privileged function table
- Launch blockers
- Documentation gaps
- Questions for the team
- Recommended next actions
""",
    "02-tokenomics-risk-review.md": """# AI Review Prompt: Tokenomics and Transfer-Risk Review

You are reviewing an ERC20/token project before launch.

Goal: identify tokenomics-related implementation risks that should be disclosed or checked before audit/mainnet.

Inputs to paste below:
- Solidity contracts
- Tokenomics notes
- DLSK findings
- Deployment checklist

Review checklist:
1. Detect supply cap, mint policy, burn policy, decimals, initial distribution, vesting, airdrop, tax/fee, blacklist/whitelist, max wallet, max transaction, anti-bot, and DEX/router behavior.
2. Identify mutable tokenomics parameters and who can change them.
3. Explain whether any mechanism could surprise users after launch.
4. Identify documentation gaps rather than making unsupported accusations.
5. Separate hard risks from normal launch-policy choices.

Output format:
- Token behavior summary
- Mutable parameters
- User-impacting powers
- Disclosure gaps
- Launch blockers
- Questions for the team
""",
    "03-upgradeability-review.md": """# AI Review Prompt: Upgradeability and Proxy Review

You are reviewing a Solidity project that may use proxies or upgradeable contracts.

Goal: identify upgradeability risks and documentation gaps before audit/mainnet.

Inputs to paste below:
- Solidity contracts
- Deployment scripts
- DLSK report
- Any proxy/admin addresses or deployment notes

Review checklist:
1. Detect UUPS, Transparent Proxy, Beacon Proxy, custom proxy, delegatecall, initializer, reinitializer, storage gaps, and implementation admin patterns.
2. Identify who can upgrade and how upgrades are authorized.
3. Check whether initialization appears protected.
4. Identify storage-layout or delegatecall areas that require expert audit.
5. Identify whether upgrade power is documented for users/investors/auditors.
6. Do not claim safety without manual verification.

Output format:
- Upgradeability summary
- Upgrade authority table
- Initialization concerns
- Storage/delegatecall concerns
- Launch blockers
- Questions for the team
""",
    "04-launch-blocker-review.md": """# AI Review Prompt: Launch-Blocker Review

You are reviewing a Solidity project immediately before testnet, mainnet, or formal audit.

Goal: produce a short launch-readiness triage, not a full audit.

Inputs to paste below:
- DLSK report.md or report.json
- DLSK checklist.md
- Contract surface map
- Project README
- Deployment assumptions

Classify each issue as:
- BLOCKER: should be fixed or explicitly accepted before mainnet.
- NEEDS TEAM CONFIRMATION: cannot decide without project context.
- DOCUMENTATION GAP: should be disclosed in audit-prep materials.
- LOW PRIORITY: can wait.

Review checklist:
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

Output format:
- Executive summary
- Blockers
- Needs confirmation
- Documentation gaps
- Suggested GitHub issue text
- Suggested auditor handoff notes
""",
    "05-audit-prep-summary.md": """# AI Review Prompt: Audit-Preparation Summary

You are helping a small DeFi/token team prepare materials for a formal security auditor.

Goal: convert DLSK outputs and project notes into a concise audit-preparation summary.

Inputs to paste below:
- README
- DLSK report
- Audit-prep pack
- Contract surface map
- Deployment checklist
- Known risks

Create:
1. Project overview.
2. Contract scope.
3. Out-of-scope items.
4. Deployment assumptions.
5. Owner/admin and governance assumptions.
6. Known risks and accepted tradeoffs.
7. Areas needing auditor attention.
8. Questions the team should answer before audit.
9. Plain-English disclaimer: this is pre-audit preparation, not a formal audit.

Output format:
- Audit prep summary
- Contract scope table
- Privileged controls summary
- Known-risk notes
- Questions for auditor
- Questions for project team
""",
}


def _iter_solidity_files(source: Path) -> list[Path]:
    if source.is_file():
        return [source]
    return sorted(source.rglob("*.sol"))


def _line_number(content: str, start: int) -> int:
    return content[:start].count("\n") + 1


def scan_sources(paths: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for severity, category, title, pattern, recommendation in RULES:
            for match in re.finditer(pattern, content, flags=re.IGNORECASE):
                findings.append(
                    Finding(
                        severity=severity,
                        category=category,
                        title=title,
                        evidence=match.group(0),
                        recommendation=recommendation,
                        file=str(path),
                        line=_line_number(content, match.start()),
                    )
                )
    return findings


def launch_checklist(paths: list[Path]) -> list[ChecklistItem]:
    names = "\n".join(str(p) for p in paths)
    root = paths[0].parent if paths else Path(".")
    root_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in paths)
    checks = [
        ("Unit tests", "FOUND" if any((root / n).exists() for n in ["test", "tests"]) else "NEEDS_MANUAL_CONFIRMATION", "Confirm Foundry/Hardhat/pytest-style tests cover privileged flows."),
        ("Deployment script", "FOUND" if "deploy" in names.lower() else "NEEDS_MANUAL_CONFIRMATION", "Keep reproducible deployment scripts and parameter logs."),
        ("Multisig ownership", "FOUND" if re.search(r"multisig|safe", root_text, re.I) else "NEEDS_MANUAL_CONFIRMATION", "Use Safe/multisig for owner/admin roles."),
        ("Timelock", "FOUND" if re.search(r"timelock", root_text, re.I) else "NEEDS_MANUAL_CONFIRMATION", "Use timelock for high-impact governance or upgrade actions."),
        ("Liquidity lock", "NEEDS_MANUAL_CONFIRMATION", "Document LP lock, vesting, and treasury controls before launch."),
        ("Known risk disclosure", "NEEDS_MANUAL_CONFIRMATION", "Write known risks and operational assumptions before audit or launch."),
    ]
    return [ChecklistItem(item=a, status=b, recommendation=c) for a, b, c in checks]


def run_slither(source: Path) -> tuple[bool, str | None]:
    if shutil.which("slither") is None:
        return False, None
    try:
        completed = subprocess.run(["slither", str(source)], capture_output=True, text=True, timeout=60)
        return True, (completed.stdout + "\n" + completed.stderr).strip()
    except Exception as exc:  # defensive: Slither must never break the built-in scanner
        return True, f"Slither failed: {exc}"


def overall_risk(findings: list[Finding]) -> str:
    if not findings:
        return "INFO"
    return max((f.severity for f in findings), key=lambda s: SEVERITY_ORDER[s])


def counts(findings: list[Finding]) -> dict[str, int]:
    result = {k: 0 for k in SEVERITY_ORDER}
    for finding in findings:
        result[finding.severity] += 1
    return result


def write_reports(out: Path, source: str, findings: list[Finding], checklist: list[ChecklistItem], slither_available: bool, slither_output: str | None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    data = {
        "source": source,
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "overall_risk": overall_risk(findings),
        "counts": counts(findings),
        "total_findings": len(findings),
        "findings": [asdict(f) for f in findings],
        "checklist": [asdict(c) for c in checklist],
        "slither_available": slither_available,
        "slither_output": slither_output,
        "ai_assisted_workflow": {
            "recommended_next_step": "Run `dlsk ai-pack --out <audit-prep-pack>/ai-review-prompts` and use the prompts with a human reviewer.",
            "disclaimer": "AI model output should be treated as review input, not proof of safety.",
        },
        "disclaimer": "Lightweight pre-audit technical review. Not a formal security audit.",
    }
    (out / "report.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# DeFi Launch Safety Review Report",
        "",
        "## 1. Summary",
        "",
        f"- Source: {source}",
        f"- Scan Time: {data['scan_time']}",
        f"- Overall Risk: **{data['overall_risk']}**",
        f"- Total Findings: {len(findings)}",
    ]
    for sev, n in data["counts"].items():
        lines.append(f"- {sev.title()}: {n}")
    lines += ["", "## 2. Key Findings", "", "| Severity | Category | Title | Evidence | Recommendation |", "|---|---|---|---|---|"]
    for f in findings:
        loc = f"<br>{f.file}:{f.line}" if f.file else ""
        lines.append(f"| {f.severity} | {f.category} | {f.title} | `{f.evidence}`{loc} | {f.recommendation} |")
    lines += ["", "## 3. Launch Checklist", "", "| Status | Item | Recommendation |", "|---|---|---|"]
    for c in checklist:
        lines.append(f"| {c.status} | {c.item} | {c.recommendation} |")
    lines += ["", "## 4. AI-Assisted Review Next Step", ""]
    lines += [
        "Run:",
        "",
        "```bash",
        "dlsk ai-pack --out ai-review-prompts",
        "```",
        "",
        "Use the generated prompts to turn this scan into a human-reviewed launch-readiness evidence pack. AI output should be treated as review input, not proof of safety.",
    ]
    lines += ["", "## 5. Slither Notes", ""]
    if slither_output:
        lines += ["```text", slither_output[:4000], "```"]
    else:
        lines.append("Slither was not run or returned no output.")
    lines += ["", "## 6. Disclaimer", "", "This report is a lightweight pre-audit technical review. It is not a formal security audit and does not guarantee the absence of vulnerabilities."]
    (out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    checklist_lines = ["# Launch Checklist", ""]
    for item in checklist:
        checklist_lines.append(f"- [{item.status}] **{item.item}** — {item.recommendation}")
    (out / "checklist.md").write_text("\n".join(checklist_lines) + "\n", encoding="utf-8")


def fetch_verified_source(address: str, chain: str) -> str:
    chain = chain.lower()
    key_env = {"ethereum": "ETHERSCAN_API_KEY", "bsc": "BSCSCAN_API_KEY", "polygon": "POLYGONSCAN_API_KEY"}.get(chain)
    base_url = {
        "ethereum": "https://api.etherscan.io/api",
        "bsc": "https://api.bscscan.com/api",
        "polygon": "https://api.polygonscan.com/api",
    }.get(chain)
    if not key_env or not base_url:
        raise typer.BadParameter("Unsupported chain. Use ethereum, bsc, or polygon.")
    api_key = os.getenv(key_env)
    if not api_key:
        raise typer.BadParameter(f"Missing {key_env}. Local --source scanning works without API keys.")
    params = {"module": "contract", "action": "getsourcecode", "address": address, "apikey": api_key}
    response = requests.get(base_url, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    result = payload.get("result") or []
    if not result or not result[0].get("SourceCode"):
        raise typer.BadParameter("No verified source code found for this address.")
    return result[0]["SourceCode"]


@app.command()
def ai_pack(
    out: Path = typer.Option(Path("ai-review-prompts"), "--out", help="Output directory for AI review prompts."),
) -> None:
    """Generate AI-assisted launch-readiness review prompts.

    The prompts are designed to be pasted into a model together with DLSK reports,
    contract maps, deployment notes, and source excerpts. They do not replace a
    formal audit or human review.
    """
    out.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# AI-Assisted Launch-Readiness Prompt Pack",
        "",
        "This pack helps turn DLSK scan output into a human-reviewed launch-readiness evidence pack.",
        "",
        "Use these prompts with your preferred AI model together with:",
        "",
        "- `report.md` or `report.json`",
        "- `checklist.md`",
        "- contract surface map",
        "- deployment scripts and assumptions",
        "- known-risk notes",
        "",
        "Important: AI output is review input, not proof of safety. This pack is not a formal security audit.",
        "",
        "## Prompts",
        "",
    ]

    for filename, content in AI_REVIEW_PROMPTS.items():
        (out / filename).write_text(content.strip() + "\n", encoding="utf-8")
        title = content.splitlines()[0].lstrip("# ").strip()
        index_lines.append(f"- [{title}]({filename})")

    index_lines += [
        "",
        "## Suggested workflow",
        "",
        "1. Run `dlsk scan --format all`.",
        "2. Run `dlsk map` or prepare a contract surface summary.",
        "3. Run `dlsk prep` if available for the project.",
        "4. Run `dlsk ai-pack --out ai-review-prompts`.",
        "5. Paste one prompt at a time into your AI model with the relevant evidence.",
        "6. Keep only reviewed, confirmed items in the final launch-readiness evidence pack.",
    ]

    (out / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    console.print(f"[green]AI review prompt pack written to[/green] {out}")


@app.command()
def scan(
    source: Path | None = typer.Option(None, "--source", help="Solidity file or directory to scan."),
    address: str | None = typer.Option(None, "--address", help="Verified contract address to fetch from explorer."),
    chain: str = typer.Option("ethereum", "--chain", help="ethereum, bsc, or polygon."),
    out: Path = typer.Option(Path("reports/latest"), "--out", help="Output directory."),
    format: str = typer.Option("all", "--format", help="all, markdown, or json."),
    no_slither: bool = typer.Option(False, "--no-slither", help="Disable optional Slither execution."),
) -> None:
    """Scan Solidity source and generate a launch safety report."""
    if not source and not address:
        raise typer.BadParameter("Provide --source or --address.")

    temp_file: Path | None = None
    if address:
        fetched = fetch_verified_source(address, chain)
        out.mkdir(parents=True, exist_ok=True)
        temp_file = out / f"{address}.sol"
        temp_file.write_text(fetched, encoding="utf-8")
        source = temp_file

    assert source is not None
    paths = _iter_solidity_files(source)
    if not paths:
        raise typer.BadParameter(f"No Solidity files found in {source}")

    findings = scan_sources(paths)
    checklist = launch_checklist(paths)
    slither_available, slither_output = (False, None) if no_slither else run_slither(source)
    write_reports(out, str(source), findings, checklist, slither_available, slither_output)

    c = counts(findings)
    table = Table(title="DeFi Launch Safety Summary")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Overall Risk", overall_risk(findings))
    table.add_row("Findings", str(len(findings)))
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        table.add_row(sev.title(), str(c[sev]))
    table.add_row("Report", str(out / "report.md"))
    console.print(table)


if __name__ == "__main__":
    app()
