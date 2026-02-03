import csv
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from main import get_report, main


def test_get_report_valid():
    report = get_report("average-gdp")
    assert report is not None


def test_get_report_invalid():
    with pytest.raises(ValueError):
        get_report("invalid-report")


def test_main_success(capsys):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["country", "year", "gdp", "gdp_growth", "inflation", "unemployment", "population", "continent"],
        )
        writer.writeheader()
        writer.writerow({
            "country": "United States",
            "year": "2023",
            "gdp": "1000",
            "gdp_growth": "2.1",
            "inflation": "3.4",
            "unemployment": "3.7",
            "population": "339",
            "continent": "North America",
        })
        temp_path = f.name

    try:
        with patch.object(sys, "argv", ["main.py", "--files", temp_path, "--report", "average-gdp"]):
            main()
            captured = capsys.readouterr()
            assert "United States" in captured.out
            assert "1000" in captured.out
    finally:
        Path(temp_path).unlink()


def test_main_file_not_found(capsys):
    with patch.object(sys, "argv", ["main.py", "--files", "nonexistent.csv", "--report", "average-gdp"]):
        with pytest.raises(ValueError, match="Ошибка при загрузке файлов"):
            main()


def test_main_invalid_report(capsys):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        writer = csv.DictWriter(f, fieldnames=["country", "gdp"])
        writer.writeheader()
        writer.writerow({"country": "Test", "gdp": "1000"})
        temp_path = f.name

    try:
        with patch.object(sys, "argv", ["main.py", "--files", temp_path, "--report", "invalid"]):
            with pytest.raises(ValueError, match="не найден"):
                main()
    finally:
        Path(temp_path).unlink()
