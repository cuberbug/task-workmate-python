import pytest

from analyzer.models import Employee


CSV_HEADER = (
    "name,position,completed_tasks,performance,"
    "skills,team,experience_years"
)


@pytest.fixture
def sample_employees():
    """
    Фикстура возвращает список сотрудников для тестов отчетов.
    Данные подобраны так, чтобы удобно проверять математику:
    - Backend: (5.0 + 4.0) / 2 = 4.5
    - Frontend: 3.0 / 1 = 3.0
    """
    return [
        Employee(
            name="Alice",
            position="Backend Developer",
            completed_tasks=10,
            performance=5.0,
            skills=("Python", "Django"),
            team="Alpha",
            experience_years=5
        ),
        Employee(
            name="Bob",
            position="Backend Developer",
            completed_tasks=20,
            performance=4.0,
            skills=("Go",),
            team="Beta",
            experience_years=3
        ),
        Employee(
            name="Johnny",
            position="Frontend Developer",
            completed_tasks=15,
            performance=3.0,
            skills=("React",),
            team="Cum",
            experience_years=2
        ),
    ]


@pytest.fixture
def create_temp_csv(tmp_path):
    """
    Фикстура-фабрика. Возвращает функцию, которая создает CSV-файл.
    Автоматически добавляет заголовок и сохраняет файл во временной директории.
    """
    def _create(filename: str, rows: list[str], header: str = CSV_HEADER):
        # Собираем контент: заголовок + строки (разделитель \n)
        content = "\n".join([header] + rows)

        file_path = tmp_path / filename
        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    return _create
