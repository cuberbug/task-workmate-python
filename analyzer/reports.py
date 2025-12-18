import statistics
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any

from .models import Employee


class ReportStrategy(ABC):
    """Абстрактный базовый класс (интерфейс) для всех будущих отчетов."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Внутреннее имя отчёта (для реестра)"""
        pass

    @abstractmethod
    def generate(self, employees: list[Employee]) -> list[dict[str, Any]]:
        """
        Метод должен принять список сотрудников и вернуть список словарей
        для последующего вывода в таблицу.
        """
        pass


class PerformanceReport(ReportStrategy):
    """
    Реализация отчёта по эффективности (performance).
    Группирует по position и считает средний performance.
    """
    name = "performance"

    def generate(self, employees: list[Employee]) -> list[dict[str, Any]]:
        """
        Генерирует готовый к выводу отчёт.

        Вычисляет среднюю оценку по всем сотрудникам для каждой должности
        и сортирует их по эффективности в порядке убывания.

        Args:
            employees (list[Employee]): список сотрудников и их показателей.
        """
        grouped_data = defaultdict(list)

        for emp in employees:
            grouped_data[emp.position].append(emp.performance)

        result = []
        for position, scores in grouped_data.items():
            avg_score = statistics.mean(scores)

            result.append({
                "position": position,
                "performance": avg_score
            })

        result.sort(key=lambda x: x["performance"], reverse=True)

        return result


def get_available_reports() -> dict[str, ReportStrategy]:
    """
    Возвращает словарь с реализованными отчётами.

    Для возможности использования нового отчёта, его нужно добавить
    в словарь по аналогии с PerformanceReport.
    """
    return {
        PerformanceReport.name: PerformanceReport(),
    }
