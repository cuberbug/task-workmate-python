import sys
from unittest.mock import patch

import pytest

from analyzer.main import main


def test_main_performance_report_success(create_temp_csv, capsys):
    """
    Интеграционный тест: полный цикл работы программы.
    Создаем файл -> запускаем main -> проверяем таблицу на выходе.
    """
    rows = [
        "Alice,Backend,10,5.0,Python,A,1",
        "Bob,Backend,20,4.0,Go,A,2"
    ]
    path = create_temp_csv(filename="data.csv", rows=rows)

    test_args = ["main.py", "--files", path, "--report", "performance"]

    with patch.object(sys, 'argv', test_args):
        main()

    captured = capsys.readouterr()
    stdout = captured.out

    assert "position" in stdout
    assert "performance" in stdout
    assert "Backend" in stdout
    assert "4.50" in stdout


def test_main_duplicate_files_handling(create_temp_csv, capsys):
    """
    Проверка, что передача дублирующихся путей не портит данные.
    Если файл один и тот же, среднее значение не должно измениться.
    """
    rows_a = ["Alice,Backend,10,5.0,Python,A,1"]
    rows_b = [
        "Alex,Backend,10,4.0,Python,A,1",
        "Alex,DevOps,10,4.8,Kubernetes,A,3"
    ]
    path_a = create_temp_csv(filename="data_a.csv", rows=rows_a)
    path_b = create_temp_csv(filename="data_b.csv", rows=rows_b)

    # Передаем один и тот же путь 'path_a' дважды
    path = (path_a, path_b, path_a)
    test_args = ["main.py", "--files", *path, "--report", "performance"]

    with patch.object(sys, 'argv', test_args):
        main()

    captured = capsys.readouterr()
    stdout = captured.out
    assert "Backend" in stdout
    assert "DevOps" in stdout, (
        "Второй файл не был обработан"
    )
    # Подсчёт по Backend:
    # (5.0 + 4.0)       / 2 = 4.50  [ YES ]
    # (5.0 + 4.0 + 5.0) / 2 = 4.66  [ NO ]
    assert "4.50" in stdout, (
        "Данные испорчены, так как один файл был принят и обработан дважды"
    )


def test_main_report_not_found(capsys):
    """Проверка случая, когда запрошен несуществующий отчет."""
    test_args = [
        "main.py", "--files", "dummy.csv", "--report", "salary_report"
    ]

    with patch.object(sys, 'argv', test_args):
        # Ожидаем sys.exit(1)
        with pytest.raises(SystemExit) as excinfo:
            main()

        assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "Отчет 'salary_report' не найден" in captured.err


def test_main_no_valid_data(create_temp_csv, capsys):
    """
    Проверка случая, когда файлы пустые или не содержат валидных строк.
    Скрипт должен штатно завершиться (exit 0) и вывести предупреждение.
    """
    path = create_temp_csv(filename="empty.csv", rows=[])

    test_args = ["main.py", "--files", path, "--report", "performance"]

    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0

    captured = capsys.readouterr()
    assert "не содержат валидных данных" in captured.out


def test_main_missing_args(capsys):
    """
    Проверка, что argparse ругается при отсутствии обязательных аргументов.
    """
    test_args = ["main.py"]

    with patch.object(sys, 'argv', test_args):
        # Argparse вызывает SystemExit(2) при ошибке
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code != 0

    captured = capsys.readouterr()
    # Argparse пишет usage в stderr
    assert (
        "the following arguments are required"
    ) in captured.err or "usage:" in captured.err, (
        "Не выводится сообщение об ошибке от argparse при вызове "
        "main.py без параметров"
    )
