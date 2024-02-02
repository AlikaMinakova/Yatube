# создание моделей в бд

from django.db import models


from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.TextField()
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Введите текст статьи', help_text='Введите текст поста')
    pub_date = models.DateTimeField('Дата публикации',auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    # Post.objects.filter(text__contains='утро').filter(author='leo').filter(pub_date__range
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Выберете группу',
        help_text='Выберите группу'
    )

    def __str__(self):
        return self.text[:15]

