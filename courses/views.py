from rest_framework import viewsets
from .models import Course, Student
from .serializers import CourseSerializer, StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        course_id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')

        if course_id:
            queryset = queryset.filter(id=course_id)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer