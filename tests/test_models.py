import pytest

from models import VideoStats


def test_from_row_parses_correctly() -> None:
    row = {
        "title": "Тестовое видео",
        "ctr": "18.2",
        "retention_rate": "35",
        "views": "45200",
        "likes": "1240",
        "avg_watch_time": "4.2",
    }
    video = VideoStats.from_row(row)
    assert video.title == "Тестовое видео"
    assert video.ctr == pytest.approx(18.2)
    assert video.retention_rate == pytest.approx(35.0)


def test_from_row_raises_on_invalid_float() -> None:
    row = {"title": "Bad", "ctr": "not_a_number", "retention_rate": "35"}
    with pytest.raises(ValueError):
        VideoStats.from_row(row)


def test_video_stats_is_immutable(clickbait_video: VideoStats) -> None:
    with pytest.raises((AttributeError, TypeError)):
        clickbait_video.ctr = 99.9
