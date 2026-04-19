from abc import ABC, abstractmethod
from models import VideoStats


class BaseReport(ABC):

    @abstractmethod
    def filter(self, videos: list[VideoStats]) -> list[VideoStats]:
        pass

    @abstractmethod
    def sort(self, videos: list[VideoStats]) -> list[VideoStats]:
        pass

    @abstractmethod
    def headers(self) -> list[str]:
        pass

    @abstractmethod
    def rows(self, videos: list[VideoStats]) -> list[list[str | float]]:
        pass

    def build(
        self, videos: list[VideoStats]
    ) -> tuple[list[str], list[list[str | float]]]:
        filtered = self.filter(videos)
        sorted_videos = self.sort(filtered)
        return self.headers(), self.rows(sorted_videos)
