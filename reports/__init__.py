from reports.base import BaseReport
from reports.clickbait import ClickbaitReport

# Чтобы добавить новый отчёт — добавьте его имя и класс сюда.
REPORT_REGISTRY: dict[str, type[BaseReport]] = {
    "clickbait": ClickbaitReport,
}

__all__ = ["REPORT_REGISTRY", "BaseReport", "ClickbaitReport"]
