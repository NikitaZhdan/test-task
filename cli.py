import argparse
import sys
from pathlib import Path

from reports import REPORT_REGISTRY


def _validate_files(paths: list[str]) -> list[Path]:

    resolved: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            sys.exit(f"ошибка: файл не найден: {raw!r}")
        if not p.is_file():
            sys.exit(f"ошибка: путь не является файлом: {raw!r}")
        resolved.append(p)
    return resolved


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yt-clickbait",
        description="Анализирует CSV-файлы со статистикой YouTube и формирует отчёты.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        metavar="ФАЙЛ",
        required=True,
        help="Один или несколько путей к CSV-файлам со статистикой.",
    )
    parser.add_argument(
        "--report",
        choices=list(REPORT_REGISTRY),
        required=True,
        metavar=f"{{{','.join(REPORT_REGISTRY)}}}",
        help=f"Тип отчёта. Доступные значения: {', '.join(REPORT_REGISTRY)}.",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> tuple[list[Path], str]:

    parser = build_parser()
    args = parser.parse_args(argv)
    paths = _validate_files(args.files)
    return paths, args.report
