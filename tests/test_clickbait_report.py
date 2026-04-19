import pytest

from models import VideoStats
from reports.clickbait import ClickbaitReport


@pytest.fixture()
def report() -> ClickbaitReport:
    return ClickbaitReport()


def test_filter_keeps_clickbait(
    report: ClickbaitReport, clickbait_video: VideoStats
) -> None:
    result = report.filter([clickbait_video])
    assert clickbait_video in result


def test_filter_removes_non_clickbait(
    report: ClickbaitReport,
    non_clickbait_video: VideoStats,
) -> None:
    result = report.filter([non_clickbait_video])
    assert result == []


def test_filter_excludes_borderline_ctr(
    report: ClickbaitReport,
    borderline_ctr_video: VideoStats,
) -> None:

    result = report.filter([borderline_ctr_video])
    assert result == []


def test_filter_excludes_borderline_retention(
    report: ClickbaitReport,
    borderline_retention_video: VideoStats,
) -> None:

    result = report.filter([borderline_retention_video])
    assert result == []


def test_sort_orders_by_ctr_descending(report: ClickbaitReport) -> None:
    videos = [
        VideoStats("Low", 16.0, 30.0),
        VideoStats("High", 25.0, 20.0),
        VideoStats("Mid", 20.0, 25.0),
    ]
    sorted_videos = report.sort(videos)
    ctrs = [v.ctr for v in sorted_videos]
    assert ctrs == sorted(ctrs, reverse=True)


def test_headers_returns_three_columns(report: ClickbaitReport) -> None:
    assert len(report.headers()) == 3


def test_build_returns_only_clickbait(
    report: ClickbaitReport,
    mixed_videos: list[VideoStats],
) -> None:
    headers, rows = report.build(mixed_videos)
    assert len(rows) == 1
    assert rows[0][0] == "Кликбейт видео"


def test_build_empty_input(report: ClickbaitReport) -> None:
    headers, rows = report.build([])
    assert rows == []
    assert isinstance(headers, list)


def test_build_preserves_sort_order(report: ClickbaitReport) -> None:
    videos = [
        VideoStats("B", 18.0, 30.0),
        VideoStats("A", 24.0, 22.0),
        VideoStats("C", 20.0, 35.0),
    ]
    _, rows = report.build(videos)
    ctrs = [row[1] for row in rows]
    assert ctrs == sorted(ctrs, reverse=True)
