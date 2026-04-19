from pathlib import Path

import pytest

from cli import build_parser, parse_args


def test_parse_args_valid(sample_csv_file: Path) -> None:
    paths, report = parse_args(
        ["--files", str(sample_csv_file), "--report", "clickbait"]
    )
    assert report == "clickbait"
    assert paths == [sample_csv_file]


def test_parse_args_multiple_files(
    sample_csv_file: Path, second_csv_file: Path
) -> None:
    paths, report = parse_args(
        ["--files", str(sample_csv_file), str(second_csv_file), "--report", "clickbait"]
    )
    assert len(paths) == 2


def test_parse_args_missing_files_flag() -> None:
    with pytest.raises(SystemExit):
        parse_args(["--report", "clickbait"])


def test_parse_args_missing_report_flag(sample_csv_file: Path) -> None:
    with pytest.raises(SystemExit):
        parse_args(["--files", str(sample_csv_file)])


def test_parse_args_invalid_report(sample_csv_file: Path) -> None:
    with pytest.raises(SystemExit):
        parse_args(["--files", str(sample_csv_file), "--report", "nonexistent_report"])


def test_parse_args_nonexistent_file() -> None:
    with pytest.raises(SystemExit, match="файл не найден"):
        parse_args(["--files", "/no/such/file.csv", "--report", "clickbait"])


def test_parse_args_path_is_directory(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="не является файлом"):
        parse_args(["--files", str(tmp_path), "--report", "clickbait"])


def test_build_parser_report_choices() -> None:
    parser = build_parser()
    report_action = next(
        a for a in parser._actions if "--report" in getattr(a, "option_strings", [])
    )
    assert "clickbait" in report_action.choices
