from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    """
    Модель данных сотрудника.

    Используется для жёсткой фиксации типов обрабатываемых данных
    и предупреждения свзанных с этим ошибок.
    """
    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: tuple[str, ...]
    team: str
    experience_years: int
