import csv
from pathlib import Path

from models import VideoStats


class CSVReader:

    def __init__(self, path: Path) -> None:
        self._path = path

    def read(self) -> list[VideoStats]:
        videos: list[VideoStats] = []
        with self._path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                videos.append(VideoStats.from_row(row))
        return videos
