import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from courses.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def _course_factory(**kwargs):
        return baker.make(Course, **kwargs)
    return _course_factory


@pytest.fixture
def student_factory():
    def _student_factory(**kwargs):
        return baker.make(Student, **kwargs)
    return _student_factory