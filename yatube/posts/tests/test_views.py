from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        response = self.client.get('/exist-page/')
        self.assertEqual(response.status_code, 404)
        template = 'core/404.html'
        self.assertTemplateUsed(response, template)
        # Проверьте, что статус ответа сервера - 404
        # Проверьте, что используется шаблон core/404.html
