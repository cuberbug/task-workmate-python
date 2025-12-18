import argparse
import sys

from tabulate import tabulate

from .loader import load_employees
from .reports import get_available_reports


def main():
    """
    Основная функция запуска анализатора.

    Обрабатывает аргументы командной строки, загружает данные
    и выводит запрошенный отчет.
    """
    parser = argparse.ArgumentParser(
        description="Анализ эффективности работы сотрудников."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Путь к одному или нескольким csv-файлам с данными сотрудников."
    )
    parser.add_argument(
        "--report",
        type=str,
        required=True,
        help="Название отчета для формирования (например, performance)."
    )

    args = parser.parse_args()

    available_reports = get_available_reports()
    report_name = args.report.lower()

    if report_name not in available_reports:
        print(
            f"Ошибка: Отчет '{args.report}' не найден.\n"
            f"Доступные отчеты: {', '.join(available_reports.keys())}",
            file=sys.stderr
        )
        sys.exit(1)

    employees = load_employees(args.files)

    if not employees:
        print(
            "Предупреждение: Файлы не содержат валидных данных о сотрудниках."
        )
        sys.exit(0)

    strategy = available_reports[report_name]
    report_data = strategy.generate(employees)

    if not report_data:
        print("Отчет пуст (нет данных для отображения).")
        sys.exit(0)

    print(
        tabulate(
            report_data,
            headers="keys",
            tablefmt="simple",
            showindex=range(1, len(report_data) + 1),
            floatfmt=".2f"
        )
    )


# Этот блок if __name__ == "__main__": нужен для локальных тестов модуля,
# но основной запуск будет происходить из корневого файла main.py
if __name__ == "__main__":
    main()
