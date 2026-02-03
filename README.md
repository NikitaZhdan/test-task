# Обработка макроэкономических данных

Скрипт для обработки CSV-файлов с макроэкономическими данными и генерации отчетов.

## Установка

```bash
poetry install --no-root
```
или 
```bash
pip install -r requiremets.txt
```

## Использование

### Параметры

- `--files` - пути к CSV файлам с данными (можно указать несколько файлов)
- `--report` - название отчета для генерации (доступные: `average-gdp`)

### Пример запуска

```bash
python main.py --files dataset1.csv dataset2.csv --report average-gdp
```

Скрипт выведет таблицу со странами и их средним ВВП, отсортированную по убыванию ВВП.

## Формат данных

CSV файлы должны содержать следующие колонки:
- `country` - название страны
- `year` - год
- `gdp` - ВВП
- `gdp_growth` - рост ВВП
- `inflation` - инфляция
- `unemployment` - безработица
- `population` - население
- `continent` - континент

## Добавление нового отчета

Для добавления нового отчета:

1. Создайте новый класс в модуле `reports`, наследующийся от `BaseReport`
2. Реализуйте методы `generate()` и `get_headers()`
3. Зарегистрируйте отчет в функции `get_report()` в `main.py`

Пример:

```python
# reports/new_report.py
from reports.base import BaseReport

class NewReport(BaseReport):
    def generate(self, data):
        # ваша логика генерации отчета
        return results
    
    def get_headers(self):
        return ["column1", "column2"]
```

Затем добавьте в `main.py`:
```python
from reports.new_report import NewReport

reports = {
    "average-gdp": AverageGdpReport,
    "new-report": NewReport,  # добавьте здесь
}
```

## Тестирование

Запуск тестов:
```bash
pytest
```

Запуск тестов с покрытием:
```bash
pytest --cov=. --cov-report=term-missing
```
