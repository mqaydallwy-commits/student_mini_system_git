"""Smoke tests for the application package and domain model."""
import pytest

from app.core.exceptions import InvalidGradeError
from app.models.student import Student


def test_cli_imports_successfully():
    from app.cli.menu import Application

    assert Application.__name__ == "Application"


def test_student_grade_and_average():
    student = Student("STD-1", "Ali", 20, "AI")
    student.set_grade("CRS-1", 90)
    student.set_grade("CRS-2", 80)

    assert student.average() == 85


def test_invalid_grade_is_rejected():
    student = Student("STD-1", "Ali", 20, "AI")

    with pytest.raises(InvalidGradeError):
        student.set_grade("CRS-1", 101)
