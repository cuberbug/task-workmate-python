import csv
import sys
from pathlib import Path

from .models import Employee


def _parse_skills(skills_str: str) -> tuple[str, ...]:
    """
    Парсит строку навыков в кортеж уникальных значений.

    Пример: "Python, Django, Python " -> ("Django", "Python")
    """
    if not skills_str:
        return ()

    # 1. Разбиваем по запятой
    # 2. Убираем пробелы вокруг (strip)
    # 3. Помещаем в set для удаления дублей
    # 4. Сортируем
    # 5. Превращаем в tuple
    unique_skills = set(
        s.strip() for s in skills_str.split(",") if s.strip()
    )
    return tuple(sorted(unique_skills))


def load_employees(file_paths: list[str]) -> list[Employee]:
    """
    Читает список CSV файлов и возвращает список объектов Employee.

    Если файл не найден или имеет неверный формат, скрипт выводит ошибку
    в stderr и завершает работу. Избавляется от дубликатов путей во вводе,
    сохраняя порядок принятых файлов.
    """
    employees: list[Employee] = []
    # Убираем дубликаты с сохранением порядка и преобразуем в tuple
    file_paths = tuple(dict.fromkeys(file_paths))

    for file_path in file_paths:
        path = Path(file_path)

        if not path.exists():
            print(f"Ошибка: Файл '{file_path}' не найден.", file=sys.stderr)
            sys.exit(1)

        try:
            with path.open(mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)

                # Валидация заголовков
                required_fields = {
                    "name",
                    "position",
                    "completed_tasks",
                    "performance",
                    "skills",
                    "team",
                    "experience_years"
                }
                fields = reader.fieldnames
                if not fields or not required_fields.issubset(fields):
                    print(
                        f"Ошибка: В файле '{file_path}' отсутствуют "
                        "обязательные колонки.",
                        file=sys.stderr
                    )
                    sys.exit(1)

                for row_num, row in enumerate(reader, start=2):
                    try:
                        emp = Employee(
                            name=row["name"],
                            position=row["position"],
                            completed_tasks=int(row["completed_tasks"]),
                            performance=float(row["performance"]),
                            skills=_parse_skills(row["skills"]),
                            team=row["team"],
                            experience_years=int(row["experience_years"])
                        )
                        employees.append(emp)
                    except ValueError as e:
                        print(
                            "Предупреждение: Ошибка данных в файле "
                            f"'{file_path}' строка {row_num}: {e}",
                            file=sys.stderr
                        )
                        continue

        except Exception as e:
            print(
                f"Критическая ошибка при чтении файла '{file_path}': {e}",
                file=sys.stderr)
            sys.exit(1)

    return employees
