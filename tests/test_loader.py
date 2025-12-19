import pytest

from analyzer.loader import load_employees, _parse_skills


# --- Тесты вспомогательных функций ---

def test_parse_skills_basic():
    """Проверка парсинга, удаления дублей и сортировки."""
    raw = " Python, Django,  Python "
    result = _parse_skills(raw)
    assert len(result) == 2, (
        "Дубликаты скиллов не удаляются"
    )
    assert result == ("Django", "Python"), (
        "Сортировка скиллов не работает"
    )


def test_parse_skills_empty():
    assert _parse_skills("") == ()
    assert _parse_skills("   ") == ()


# --- Тесты загрузчика (с временными файлами) ---

def test_load_employees_valid(create_temp_csv):
    """Проверка успешного чтения валидного CSV."""
    rows = ["John Doe,Dev,10,4.5,\"Python, SQL\",Team A,3"]
    path = create_temp_csv(filename="test.csv", rows=rows)

    employees = load_employees([path])

    assert len(employees) == 1
    assert employees[0].name == "John Doe"
    assert employees[0].skills == ("Python", "SQL")


def test_load_employees_file_not_found(capsys):
    """Проверка выхода (SystemExit) если файл не найден."""
    with pytest.raises(SystemExit) as excinfo:
        load_employees(["non_existent_file.csv"])

    assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "не найден" in captured.err


def test_load_employees_bad_headers(create_temp_csv, capsys):
    """Проверка выхода, если заголовки неверные."""
    path = create_temp_csv(
        filename="bad.csv",
        rows=["1,2"],
        header="wrong,headers"
    )

    with pytest.raises(SystemExit):
        load_employees([path])

    captured = capsys.readouterr()
    assert "отсутствуют обязательные колонки" in captured.err


def test_load_employees_corrupted_row(create_temp_csv, capsys):
    """
    Проверка пропуска битой строки.

    Битая строка должна быть пропущена, но остальные читаться.
    В stderr должно уйти предупреждение.
    """
    rows = [
        "Good,Dev,10,5.0,Skill,A,1",
        "Bad,Dev,TEN,5.0,Skill,A,1",  # Битая строка
        "Good2,Dev,20,4.0,Skill,A,2"
    ]
    path = create_temp_csv(filename="mixed.csv", rows=rows)

    employees = load_employees([path])

    assert len(employees) == 2
    assert employees[0].name == "Good"
    assert employees[1].name == "Good2"

    captured = capsys.readouterr()
    assert "Ошибка данных" in captured.err


def test_load_employees_deduplicates_paths(create_temp_csv):
    """Проверка, что функция загрузки игнорирует повторяющиеся пути."""
    rows = ["John Doe,Dev,10,4.5,Python,Team A,3"]
    path = create_temp_csv("test.csv", rows)

    # Загружаем дважды один и тот же путь
    employees = load_employees([path, path])

    # В списке должен быть 1 сотрудник, а не 2
    assert len(employees) == 1, (
        "Один файл был принят и обработан дважды"
    )
