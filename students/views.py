# views.py
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from students.filters import CourseFilter
from students.models import Course
from students.serializers import CourseSerializer


class CoursesViewSet(viewsets.ModelViewSet):
    """ViewSet для Courses"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CourseFilter
    search_fields = ['name']

