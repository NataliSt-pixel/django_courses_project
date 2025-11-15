import pytest
from rest_framework.test import APIClient
from courses.models import Course
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_courses.settings')
django.setup()


@pytest.mark.django_db
def test_course_creation():
    """Тест создания курса через модель"""
    course = Course.objects.create(
        name="Test Course",
        description="Test Description", 
        start_date="2023-01-01T00:00:00Z",
        end_date="2023-12-31T00:00:00Z"
    )
    assert course.name == "Test Course"
    assert Course.objects.count() == 1
    print("✓ Course creation works")


@pytest.mark.django_db
def test_courses_list_api():
    """Тест API списка курсов"""
    client = APIClient()

    course = Course.objects.create(
        name="API Test Course",
        start_date="2023-01-01T00:00:00Z",
        end_date="2023-12-31T00:00:00Z"
    )

    response = client.get('/api/courses/')
    
    print(f"API Response status: {response.status_code}")
    print(f"API Response data: {response.data}")
    
    if response.status_code == 200:
        assert len(response.data) >= 1
        assert any(c['name'] == 'API Test Course' for c in response.data)
        print("✓ Courses list API works")
    else:
        pytest.fail(f"API returned status {response.status_code}")


@pytest.mark.django_db
def test_course_detail_api():
    """Тест API деталей курса"""
    client = APIClient()
    
    course = Course.objects.create(
        name="Detail Test Course",
        start_date="2023-01-01T00:00:00Z",
        end_date="2023-12-31T00:00:00Z"
    )
    
    response = client.get(f'/api/courses/{course.id}/')
    
    print(f"Detail API Response status: {response.status_code}")
    
    if response.status_code == 200:
        assert response.data['name'] == 'Detail Test Course'
        print("✓ Course detail API works")
    else:
        pytest.fail(f"Detail API returned status {response.status_code}")
