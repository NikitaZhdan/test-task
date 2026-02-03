import csv
import tempfile
from pathlib import Path

import pytest

from data_loader import load_csv_files


def test_load_single_csv_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["country", "year", "gdp", "gdp_growth", "inflation", "unemployment", "population", "continent"],
        )
        writer.writeheader()
        writer.writerow({
            "country": "United States",
            "year": "2023",
            "gdp": "25462",
            "gdp_growth": "2.1",
            "inflation": "3.4",
            "unemployment": "3.7",
            "population": "339",
            "continent": "North America",
        })
        temp_path = f.name

    try:
        data = load_csv_files([temp_path])
        assert len(data) == 1
        assert data[0]["country"] == "United States"
        assert data[0]["gdp"] == "25462"
    finally:
        Path(temp_path).unlink()


def test_load_multiple_csv_files():
    temp_files = []
    try:
        for i in range(2):
            f = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
            writer = csv.DictWriter(f, fieldnames=["country", "year", "gdp"])
            writer.writeheader()
            writer.writerow({"country": f"Country{i}", "year": "2023", "gdp": "1000"})
            temp_files.append(f.name)
            f.close()

        data = load_csv_files(temp_files)
        assert len(data) == 2
        assert data[0]["country"] == "Country0"
        assert data[1]["country"] == "Country1"
    finally:
        for path in temp_files:
            Path(path).unlink()


def test_load_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        load_csv_files(["nonexistent_file.csv"])


def test_load_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        temp_path = f.name

    try:
        with pytest.raises(ValueError):
            load_csv_files([temp_path])
    finally:
        Path(temp_path).unlink()


def test_load_directory_instead_of_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(ValueError, match="не является файлом"):
            load_csv_files([temp_dir])