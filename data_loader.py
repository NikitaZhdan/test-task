import csv
from pathlib import Path

def load_csv_files(file_paths):

    all_data = []

    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")


        if not path.is_file():
            raise ValueError(f"Путь не является файлом: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            if not rows:
                raise ValueError(f"Файл пуст: {file_path}")

            all_data.extend(rows)

    return all_data
