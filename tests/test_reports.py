import pytest

from reports.average_gdp import AverageGdpReport
from reports.base import BaseReport


def test_average_gdp_report_single_country():
    report = AverageGdpReport()
    data = [
        {"country": "United States", "gdp": "1000"},
        {"country": "United States", "gdp": "2000"},
        {"country": "United States", "gdp": "3000"},
    ]

    results = report.generate(data)
    assert len(results) == 1
    assert results[0]["country"] == "United States"
    assert results[0]["gdp"] == 2000.0


def test_average_gdp_report_multiple_countries():
    report = AverageGdpReport()
    data = [
        {"country": "United States", "gdp": "1000"},
        {"country": "United States", "gdp": "2000"},
        {"country": "China", "gdp": "5000"},
        {"country": "China", "gdp": "3000"},
    ]

    results = report.generate(data)
    assert len(results) == 2
    assert results[0]["country"] == "China"
    assert results[0]["gdp"] == 4000.0
    assert results[1]["country"] == "United States"
    assert results[1]["gdp"] == 1500.0


def test_average_gdp_report_sorting():
    report = AverageGdpReport()
    data = [
        {"country": "Small", "gdp": "100"},
        {"country": "Large", "gdp": "1000"},
        {"country": "Medium", "gdp": "500"},
    ]

    results = report.generate(data)
    assert results[0]["country"] == "Large"
    assert results[1]["country"] == "Medium"
    assert results[2]["country"] == "Small"


def test_average_gdp_report_missing_data():
    report = AverageGdpReport()
    data = [
        {"country": "United States", "gdp": "1000"},
        {"country": "United States"},  # пропущен gdp
        {"country": "", "gdp": "2000"},
    ]

    results = report.generate(data)
    assert len(results) == 1
    assert results[0]["country"] == "United States"
    assert results[0]["gdp"] == 1000.0


def test_average_gdp_report_invalid_gdp():
    report = AverageGdpReport()
    data = [
        {"country": "United States", "gdp": "1000"},
        {"country": "United States", "gdp": "invalid"},
        {"country": "United States", "gdp": "2000"},
    ]

    results = report.generate(data)
    assert len(results) == 1
    assert results[0]["country"] == "United States"
    assert results[0]["gdp"] == 1500.0


def test_average_gdp_report_empty_data():
    report = AverageGdpReport()
    data = []
    results = report.generate(data)
    assert len(results) == 0


def test_average_gdp_report_headers():
    report = AverageGdpReport()
    assert report.get_headers() == ["country", "gdp"]
