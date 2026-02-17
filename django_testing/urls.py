from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import CoursesViewSet


router = DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='course')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]



