import pytest
from model_bakery import baker
from courses.models import Course


@pytest.mark.django_db
def test_simple_factory():
    """Простой тест с factory"""
    course = baker.make(Course)
    assert course.id is not None
    assert isinstance(course.name, str)
    print(f"✓ Factory created course: {course.name}")


@pytest.mark.django_db
def test_factory_with_parameters():
    """Тест factory с параметрами"""
    course = baker.make(Course, name="Test Course")
    assert course.name == "Test Course"
    print("✓ Factory with parameters works")