# создание моделей в бд

from django.db import models


from django.contrib.auth import get_user_model

User = get_user_model()

TITLE_CHOICES = ["Literature", "News", "Painting"]

class Group(models.Model):
    title = models.TextField()
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    # Post.objects.filter(text__contains='утро').filter(author='leo').filter(pub_date__range
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text

