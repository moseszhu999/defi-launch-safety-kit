from typer.testing import CliRunner

from dlsk.cli import AI_REVIEW_PROMPTS, app


runner = CliRunner()


def test_ai_pack_generates_prompt_files(tmp_path):
    result = runner.invoke(app, ["ai-pack", "--out", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / "README.md").exists()

    for filename in AI_REVIEW_PROMPTS:
        prompt_file = tmp_path / filename
        assert prompt_file.exists()
        assert prompt_file.read_text(encoding="utf-8").startswith("# AI Review Prompt:")
