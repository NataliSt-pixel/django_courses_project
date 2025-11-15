import pytest
from courses.models import Course
from django.urls import reverse


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения первого курса (retrieve-логика)"""
    course = course_factory()

    url = reverse('course-detail', args=[course.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов (list-логика)"""
    course1 = course_factory()
    course2 = course_factory()

    url = reverse('course-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2

    course_ids = [course['id'] for course in response.data]
    assert course1.id in course_ids
    assert course2.id in course_ids


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации списка курсов по id"""
    course1 = course_factory()
    course2 = course_factory()

    url = reverse('course-list')
    response = api_client.get(url, {'id': course1.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course1.id
    assert response.data[0]['name'] == course1.name


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации списка курсов по name"""
    course1 = course_factory(name='Python Basics')
    course2 = course_factory(name='Advanced Django')

    url = reverse('course-list')
    response = api_client.get(url, {'name': 'Python'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Python Basics'


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса"""
    course_data = {
        'name': 'New Course',
        'description': 'Course Description',
        'start_date': '2023-09-01T00:00:00Z',
        'end_date': '2023-12-01T00:00:00Z'
    }

    url = reverse('course-list')
    response = api_client.post(url, course_data, format='json')

    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert Course.objects.get().name == 'New Course'


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса"""
    course = course_factory(name='Old Name')

    update_data = {
        'name': 'Updated Name',
        'description': course.description,
        'start_date': course.start_date.isoformat(),
        'end_date': course.end_date.isoformat()
    }

    url = reverse('course-detail', args=[course.id])
    response = api_client.put(url, update_data, format='json')

    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == 'Updated Name'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса"""
    course = course_factory()

    url = reverse('course-detail', args=[course.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == 0


@pytest.mark.django_db
def test_create_student(api_client, course_factory):
    """Тест создания студента"""
    course = course_factory()

    student_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'courses': [course.id]
    }

    url = reverse('student-list')
    response = api_client.post(url, student_data, format='json')

    assert response.status_code == 201
    assert response.data['name'] == 'John Doe'
    assert response.data['email'] == 'john.doe@example.com'
    assert course.id in response.data['courses']