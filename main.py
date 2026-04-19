import sys

from tabulate import tabulate

from cli import parse_args
from models import VideoStats
from reader import CSVReader
from reports import REPORT_REGISTRY


def _load_videos(paths: list) -> list[VideoStats]:

    videos: list[VideoStats] = []
    for path in paths:
        try:
            videos.extend(CSVReader(path).read())
        except KeyError as exc:
            sys.exit(f"ошибка: отсутствует колонка {exc} в файле {path}")
        except ValueError as exc:
            sys.exit(f"ошибка: некорректные данные в файле {path}: {exc}")
    return videos


def main(argv: list[str] | None = None) -> None:

    paths, report_name = parse_args(argv)
    videos = _load_videos(paths)

    report_cls = REPORT_REGISTRY[report_name]
    report = report_cls()
    headers, rows = report.build(videos)

    if not rows:
        print("Нет видео, соответствующих критериям отчёта.")
        return

    print(tabulate(rows, headers=headers, tablefmt="simple", floatfmt=".1f"))


if __name__ == "__main__":
    main()
