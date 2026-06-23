from pathlib import Path

from typer.testing import CliRunner

from dlsk.cli import app, scan_sources, _iter_solidity_files


def test_risky_token_expected_findings():
    paths = _iter_solidity_files(Path("examples/contracts/RiskyToken.sol"))
    findings = scan_sources(paths)
    joined = "\n".join(f"{f.title} {f.evidence}" for f in findings).lower()
    assert "mint" in joined
    assert "blacklist" in joined
    assert "pause" in joined
    assert "tax" in joined or "fee" in joined
    assert "onlyowner" in joined
    assert "rescuetokens" in joined or "rescue" in joined
    assert "emergencywithdraw" in joined or "emergency" in joined


def test_cli_generates_report(tmp_path):
    runner = CliRunner()
    result = runner.invoke(app, [
        "scan",
        "--source",
        "examples/contracts/RiskyToken.sol",
        "--out",
        str(tmp_path),
        "--no-slither",
    ])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "report.json").exists()
    assert (tmp_path / "checklist.md").exists()
    assert "DeFi Launch Safety Review Report" in (tmp_path / "report.md").read_text(encoding="utf-8")
