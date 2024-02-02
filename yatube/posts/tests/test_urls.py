# posts/tests/test_urls.py
from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_aythor(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_about_tech(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

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


