from pathlib import Path

import pytest

from reader import CSVReader


def test_reader_returns_all_rows(sample_csv_file: Path) -> None:
    videos = CSVReader(sample_csv_file).read()
    assert len(videos) == 3


def test_reader_parses_values_correctly(sample_csv_file: Path) -> None:
    videos = CSVReader(sample_csv_file).read()
    first = videos[0]
    assert first.title == "Кликбейт 1"
    assert first.ctr == pytest.approx(22.5)
    assert first.retention_rate == pytest.approx(28.0)


def test_reader_raises_on_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        CSVReader(Path("/nonexistent/path/stats.csv")).read()


def test_reader_uses_context_manager(
    sample_csv_file: Path, monkeypatch: pytest.MonkeyPatch
) -> None:

    opened_files: list = []
    original_open = Path.open

    def tracking_open(self: Path, *args, **kwargs):
        fh = original_open(self, *args, **kwargs)
        opened_files.append(fh)
        return fh

    monkeypatch.setattr(Path, "open", tracking_open)
    CSVReader(sample_csv_file).read()
    assert all(fh.closed for fh in opened_files)
