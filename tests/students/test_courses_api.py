# test_courses_api.py
import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def api_client():
    # Фикстура для создания APIClient
    return APIClient()


@pytest.fixture
def course_factory():
    # Фабрика для создания курсов
    def create_course(**kwargs):
        return baker.make(Course, **kwargs)
    return create_course


@pytest.fixture
def student_factory():
    # Фабрика для создания студентов
    def create_student(**kwargs):
        return baker.make(Student, **kwargs)
    return create_student


@pytest.mark.django_db
class TestCoursesAPI:
    def test_course_not_found(self, api_client):
        # Проверяем, что возвращается 404 для несуществующего курса
        url = "/api/courses/999/"
        response = api_client.get(url)
        assert response.status_code == 404

    def test_retrieve_course(self, api_client, course_factory):
        # Создаём курс через фабрику
        course = course_factory(name="Математика")

        # Строим URL и делаем запрос
        url = f"/api/courses/{course.id}/"
        response = api_client.get(url)

        # Проверяем код ответа
        assert response.status_code == 200

        # Проверяем, что вернулся именно этот курс
        assert response.data["id"] == course.id
        assert response.data["name"] == "Математика"
        assert "students" in response.data

    def test_list_courses(self, api_client, course_factory):
        # Создаём несколько курсов
        course1 = course_factory(name="Физика")
        course2 = course_factory(name="Химия")

        # Делаем запрос на список
        url = "/api/courses/"
        response = api_client.get(url)

        # Проверяем код ответа
        assert response.status_code == 200

        # Проверяем количество и содержимое
        assert len(response.data) == 2
        assert response.data[0]["name"] == "Физика"
        assert response.data[1]["name"] == "Химия"

    def test_filter_courses_by_id(self, api_client, course_factory):
        course1 = course_factory(name="Биология")
        url = "/api/courses/"
        response = api_client.get(url, data={"id": str(course1.id)})  # Преобразуем в строку
        assert len(response.data) == 1

    def test_filter_courses_by_name(self, api_client, course_factory):
        course1 = course_factory(name="История")
        url = "/api/courses/"
        response = api_client.get(url, data={"name": "История"})  # Точное совпадение
        assert len(response.data) == 1

    def test_create_course(self, api_client):
        # Подготавливаем данные для создания
        data = {
            "name": "Информатика",
            "students": []  # Можно опустить, если поле необязательное
        }

        # Делаем запрос на создание
        url = "/api/courses/"
        response = api_client.post(url, data=data, format="json")

        # Проверяем код ответа
        assert response.status_code == 201  # Created

        # Проверяем содержимое ответа
        assert response.data["name"] == "Информатика"
        assert "id" in response.data

        # Проверяем, что курс действительно создан в БД
        course = Course.objects.get(id=response.data["id"])
        assert course.name == "Информатика"

    def test_update_course(self, api_client, course_factory):
        # Создаём курс
        course = course_factory(name="Старый курс")

        # Подготавливаем данные для обновления
        data = {
            "name": "Обновлённый курс",
            "students": []  # Если нужно обновить список студентов — передайте IDs
        }

        # Делаем запрос на обновление
        url = f"/api/courses/{course.id}/"
        response = api_client.put(url, data=data, format="json")

        # Проверяем код ответа
        assert response.status_code == 200

        # Проверяем содержимое ответа
        assert response.data["name"] == "Обновлённый курс"

        # Проверяем, что данные в БД обновились
        course.refresh_from_db()
        assert course.name == "Обновлённый курс"

    def test_delete_course(self, api_client, course_factory):
        # Создаём курс
        course = course_factory(name="Для удаления")

        # Делаем запрос на удаление
        url = f"/api/courses/{course.id}/"
        response = api_client.delete(url)

        # Проверяем код ответа
        assert response.status_code == 204  # No Content

        # Проверяем, что курс удалён из БД
        assert not Course.objects.filter(id=course.id).exists()

