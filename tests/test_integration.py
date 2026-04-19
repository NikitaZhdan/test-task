from pathlib import Path

import pytest

from main import main


def test_main_prints_clickbait_table(
    sample_csv_file: Path, capsys: pytest.CaptureFixture
) -> None:
    main(["--files", str(sample_csv_file), "--report", "clickbait"])
    captured = capsys.readouterr()
    assert "Кликбейт 1" in captured.out
    assert "Кликбейт 2" in captured.out
    assert "Обычное видео" not in captured.out


def test_main_aggregates_multiple_files(
    sample_csv_file: Path,
    second_csv_file: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    main(
        ["--files", str(sample_csv_file), str(second_csv_file), "--report", "clickbait"]
    )
    captured = capsys.readouterr()
    assert "Кликбейт 3" in captured.out


def test_main_sorted_by_ctr_descending(
    sample_csv_file: Path, capsys: pytest.CaptureFixture
) -> None:
    main(["--files", str(sample_csv_file), "--report", "clickbait"])
    captured = capsys.readouterr()
    pos_1 = captured.out.index("Кликбейт 1")
    pos_2 = captured.out.index("Кликбейт 2")
    assert pos_1 < pos_2, "Higher CTR video should appear first"


def test_main_no_matches_prints_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    import csv

    path = tmp_path / "no_clickbait.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "title",
                "ctr",
                "retention_rate",
                "views",
                "likes",
                "avg_watch_time",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "title": "Честный обзор",
                "ctr": "6.0",
                "retention_rate": "91",
                "views": "100",
                "likes": "10",
                "avg_watch_time": "10",
            }
        )

    main(["--files", str(path), "--report", "clickbait"])
    captured = capsys.readouterr()
    assert "Нет видео" in captured.out


def test_main_exits_on_missing_file() -> None:
    with pytest.raises(SystemExit):
        main(["--files", "/no/such/file.csv", "--report", "clickbait"])


def test_main_exits_on_bad_report(sample_csv_file: Path) -> None:
    with pytest.raises(SystemExit):
        main(["--files", str(sample_csv_file), "--report", "totally_wrong"])
