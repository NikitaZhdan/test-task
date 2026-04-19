from dataclasses import dataclass


@dataclass(frozen=True)
class VideoStats:

    title: str
    ctr: float
    retention_rate: float

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "VideoStats":
        return cls(
            title=row["title"],
            ctr=float(row["ctr"]),
            retention_rate=float(row["retention_rate"]),
        )
