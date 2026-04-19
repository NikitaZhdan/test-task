from models import VideoStats
from reports.base import BaseReport

_CTR = 15.0
_RETENTION = 40.0


class ClickbaitReport(BaseReport):

    def filter(self, videos: list[VideoStats]) -> list[VideoStats]:
        return [v for v in videos if v.ctr > _CTR and v.retention_rate < _RETENTION]

    def sort(self, videos: list[VideoStats]) -> list[VideoStats]:
        return sorted(videos, key=lambda v: v.ctr, reverse=True)

    def headers(self) -> list[str]:
        return ["Название", "CTR (%)", "Удержание (%)"]

    def rows(self, videos: list[VideoStats]) -> list[list[str | float]]:
        return [[v.title, v.ctr, v.retention_rate] for v in videos]
