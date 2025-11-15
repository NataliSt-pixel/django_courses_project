import pytest
from django.conf import settings
from courses.models import Course, Student


@pytest.mark.django_db
def test_max_students_per_course(api_client, course_factory, student_factory):
    """Тест ограничения максимального количества студентов на курсе"""
    with pytest.Mark.django_db(settings.MAX_STUDENTS_PER_COURSE=2):
        course = course_factory()

        student1 = student_factory()
        student2 = student_factory()
        student3 = student_factory()

        course.students.add(student1, student2)

        with pytest.raises(Exception):
            course.students.add(student3)


@pytest.mark.django_db
@pytest.mark.parametrize('student_count,should_succeed', [
    (19, True),
    (20, True),
    (21, False)
])
def test_student_limit_parametrized(settings, course_factory, student_factory,
                                    student_count, should_succeed):
    """Параметризованный тест ограничения студентов"""
    settings.MAX_STUDENTS_PER_COURSE = 20

    course = course_factory()
    students = student_factory(_quantity=student_count)

    try:
        for student in students:
            course.students.add(student)
        success = True
    except Exception:
        success = False

    assert success == should_succeed