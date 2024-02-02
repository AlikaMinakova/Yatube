from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа первого теста',
        )


    def test_check_method_str_post(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        strpost = post.text
        self.assertEqual(strpost[:15], str(post))

    def test_check_method_str_group(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = PostModelTest.group
        strgroup= group.title
        self.assertEqual(strgroup, str(group))

    def test_verbose_name_post(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Введите текст статьи',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Выберете группу',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text_post(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)