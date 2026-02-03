import argparse

from tabulate import tabulate

from data_loader import load_csv_files
from reports import AverageGdpReport


def get_report(report_name):
    reports = {
        "average-gdp": AverageGdpReport
    }

    report_class = reports.get(report_name)
    if report_class is None:
        raise ValueError(
            f"Отчет '{report_name}' не найден."
        )

    return report_class()


def main():
    parser = argparse.ArgumentParser(
        description="Генерация отчетов по макроэкономическим данным"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV файлам с данными",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчета для генерации",
    )

    args = parser.parse_args()

    try:
        data = load_csv_files(args.files)
    except (FileNotFoundError, ValueError) as e:
        raise ValueError(f"Ошибка при загрузке файлов: {e}")

    try:
        report = get_report(args.report)
    except ValueError as e:
        raise ValueError(f"Ошибка: {e}")

    try:
        results = report.generate(data)
        headers = report.get_headers()

        if not results:
            print("Нет данных для отображения")
            return

        table_data = []
        for row in results:
            table_data.append([row[header] for header in headers])

        table = tabulate(
            table_data,
            headers=headers,
            tablefmt="grid",
            showindex=range(1, len(results) + 1),
        )
        print(table)
    except Exception as e:
        raise ValueError(f"Ошибка при генерации отчета: {e}")

if __name__ == "__main__":
    main()
