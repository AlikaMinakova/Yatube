# отображение формы

# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView

from django.contrib.auth.forms import PasswordChangeForm

# Импортируем PasswordChangeView, чтобы создать ему наследника
from django.contrib.auth.views import PasswordChangeView

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm



# за место view функции
class SignUp(CreateView):
    #  из какого класса взять форму
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную. из html
    # формы signup.html  <form method="post" action="{% url 'users:signup' %}">
    success_url = reverse_lazy('posts:index')
    # имя шаблона, куда будет передана переменная form с объектом HTML-формы
    template_name = 'users/signup.html'

