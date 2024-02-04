# posts/tests/test_urls.py
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        cls.group=Group.objects.create(
                title='literature',
                slug='literature',
                description='textdescription'
            )
        Post.objects.create(
            text='Тестовый текст2',
            group=cls.group,
            author=User.objects.create_user(username='tom')
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем второй клиент, который будет авторизован
        self.user = User.objects.create_user(username='user')
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    # Проверяем общедоступные страницы

# через консоль
# python manage.py shell
# from django.test import Client
# # Создаём объект класса Client(), эмулятор веб-браузера
# >>> guest_client = Client()
#
# # — Браузер, сделай GET-запрос к главной странице
# >>> response = guest_client.get('/')
#
# # Какой код вернула страница при запросе?
# >>> response.status_code


# ещё значения:
# status_code — содержит код ответа запрошенного адреса;
# client — объект клиента, который использовался для обращения;
# content — данные ответа в виде строки байтов;
# context — словарь переменных, переданный для отрисовки шаблона при вызове функции render();
# request — объект request, первый параметр view-функции, обработавшей запрос;
# templates — перечень шаблонов, вызванных для отрисовки запрошенной страницы;
# resolver_match — специальный объект, соответствующий path() из списка urlpatterns.


# запуск этого теста
# # Запустит все тесты проекта
# python3 manage.py test
#
# # Запустит только тесты в приложении posts
# python3 manage.py test posts
#
# # Запустит только тесты из файла test_urls.py в приложении posts
# python3 manage.py test posts.tests.test_urls
#
# # Запустит только тесты из класса StaticURLTests для test_urls.py в приложении posts
# python3 manage.py test posts.tests.test_urls.StaticURLTests
#
# # Запустит только тест test_homepage()
# # из класса StaticURLTests для test_urls.py в приложении posts
# python3 manage.py test posts.tests.test_urls.StaticURLTests.test_homepage
