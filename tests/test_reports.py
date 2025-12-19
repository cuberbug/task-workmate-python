from analyzer.reports import PerformanceReport


def test_performance_report_calculation(sample_employees):
    """Проверка математики среднего значения и группировки."""
    report = PerformanceReport()
    data = report.generate(sample_employees)

    # Ожидаем 2 записи: Backend и Frontend
    assert len(data) == 2

    # Проверяем Backend Developer
    # Сортировка по убыванию, поэтому Backend (4.5) должен быть первым,
    # Frontend (3.0) вторым
    backend_row = data[0]
    assert backend_row["position"] == "Backend Developer"
    # (5.0 + 4.0) / 2 = 4.5
    assert backend_row["performance"] == 4.5, (
        "Неправильно считается средняя эффективность"
    )

    # Проверяем Frontend Developer
    frontend_row = data[1]
    assert frontend_row["position"] == "Frontend Developer"
    assert frontend_row["performance"] == 3.0


def test_performance_report_sorting(sample_employees):
    """Проверка сортировки (от большего к меньшему)."""
    report = PerformanceReport()
    data = report.generate(sample_employees)

    # 4.5 > 3.0
    assert data[0]["performance"] > data[1]["performance"], (
        "Не работает сортировка эффективности по убыванию"
    )


def test_empty_report():
    """Проверка поведения на пустом списке."""
    report = PerformanceReport()
    data = report.generate([])
    assert data == []
