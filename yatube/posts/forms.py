from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:

        # На основе какой модели создаётся класс формы
        model = Post
        # Укажем, какие поля будут в форме
        fields = ('text', 'group', 'image')

        # Метод-валидатор для поля text
    def clean_subject(self):
        text = self.cleaned_data['text']

            # Если пользователь не поблагодарил администратора - считаем это ошибкой
        if text == '':
            raise forms.ValidationError('Вы обязательно должны заполнить это поле')

            # Метод-валидатор обязательно должен вернуть очищенные данные,
            # даже если не изменил их
        return text