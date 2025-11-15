import pytest
import django
from django.conf import settings

def test_django_installed():
    """Проверяем что Django установлен"""
    assert django.VERSION[0] >= 4
    print("Django version:", django.get_version())

def test_django_configured():
    """Проверяем что Django настроен"""
    assert settings.configured is True
    assert hasattr(settings, 'DATABASES')
    print("Django configured correctly")

def test_settings():
    """Проверяем основные настройки"""
    assert settings.DEBUG is True
    assert 'courses' in settings.INSTALLED_APPS
    assert 'rest_framework' in settings.INSTALLED_APPS
    print("Settings are correct")

@pytest.mark.django_db
def test_database_connection():
    """Проверяем подключение к базе данных"""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    assert result[0] == 1
    print("Database connection works")

@pytest.mark.django_db  
def test_course_model():
    """Проверяем модель Course"""
    from courses.models import Course
    count = Course.objects.count()
    assert count >= 0
    print("Course model works")
