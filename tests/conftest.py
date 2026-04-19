import csv
from pathlib import Path

import pytest

from models import VideoStats


@pytest.fixture()
def clickbait_video() -> VideoStats:
    return VideoStats(title="Кликбейт видео", ctr=22.5, retention_rate=28.0)


@pytest.fixture()
def non_clickbait_video() -> VideoStats:
    return VideoStats(title="Честный обзор", ctr=6.0, retention_rate=91.0)


@pytest.fixture()
def borderline_ctr_video() -> VideoStats:
    return VideoStats(title="На грани CTR", ctr=15.0, retention_rate=30.0)


@pytest.fixture()
def borderline_retention_video() -> VideoStats:
    return VideoStats(title="На грани удержания", ctr=20.0, retention_rate=40.0)


@pytest.fixture()
def mixed_videos(
    clickbait_video: VideoStats,
    non_clickbait_video: VideoStats,
) -> list[VideoStats]:
    return [clickbait_video, non_clickbait_video]


@pytest.fixture()
def sample_csv_file(tmp_path: Path) -> Path:
    rows = [
        {
            "title": "Кликбейт 1",
            "ctr": "22.5",
            "retention_rate": "28",
            "views": "100",
            "likes": "10",
            "avg_watch_time": "3",
        },
        {
            "title": "Кликбейт 2",
            "ctr": "18.0",
            "retention_rate": "35",
            "views": "200",
            "likes": "20",
            "avg_watch_time": "4",
        },
        {
            "title": "Обычное видео",
            "ctr": "9.5",
            "retention_rate": "82",
            "views": "300",
            "likes": "30",
            "avg_watch_time": "8",
        },
    ]
    path = tmp_path / "stats.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.fixture()
def second_csv_file(tmp_path: Path) -> Path:
    rows = [
        {
            "title": "Кликбейт 3",
            "ctr": "25.0",
            "retention_rate": "22",
            "views": "50",
            "likes": "5",
            "avg_watch_time": "2",
        },
    ]
    path = tmp_path / "stats2.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return path
