# обработчики url адресов

import datetime
from django.core.paginator import Paginator
from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from .forms import PostForm
from .models import Post, Group

from django.shortcuts import redirect


#декоратор который проверяет зарегистрирован ли пользователь
def authorized_only(func):
    # Функция-обёртка в декораторе может быть названа как угодно
    def check_user(request, *args, **kwargs):
        # В любую view-функции первым аргументом передаётся объект request,
        # в котором есть булева переменная is_authenticated,
        # определяющая, авторизован ли пользователь.
        if request.user.is_authenticated:
            # Возвращает view-функцию, если пользователь авторизован.
            return func(request, *args, **kwargs)
        # Если пользователь не авторизован — отправим его на страницу логина.
        return redirect('/auth/login/')
    return check_user


# Главная страница
#@authorized_only
def index(request):
    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию (от больших значений к меньшим)
    keyword = "утро"
    start_date = datetime.date(1854, 7, 7)
    end_date = datetime.date(1854, 7, 21)
    posts = Post.objects.filter(text__contains=keyword).filter(
        pub_date__range=(start_date, end_date))
    # В словаре context отправляем информацию в шаблон
    context = {
        'posts': posts,
        'title': 'Последние обновления на сайте',
        'keyword': keyword
    }
    #работа с паджинатором
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
        'title': 'Последние обновления на сайте',
    }

    return render(request, 'posts/index.html', context)


# View-функция для страницы сообщества:
def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
        'title': f'Записи сообщества {group}',
    }

    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all().filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': f'Записи сообщества {group}',
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    # Здесь код запроса к модели и создание словаря контекста
    post_list = Post.objects.all().filter(author=author).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': f'профайл пользователя {username}',
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.filter(id=post_id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):

    # Создаём объект формы

    # Проверяем, получен POST-запрос или какой-то другой:
    if request.method == 'POST':
        # Создаём объект формы класса ContactForm
        # и передаём в него полученные данные
        form = PostForm(request.POST)

        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            form.text = form.cleaned_data['text']
            form.group = form.cleaned_data['group']
            # При необходимости обрабатываем данные
            # ...
            # сохраняем объект в базу
            post = form.save(False)
            post.author = request.user
            post.save()

            # Функция redirect перенаправляет пользователя
            # на другую страницу сайта, чтобы защититься
            # от повторного заполнения формы
            return redirect(f'/profile/{request.user.username}/')

        # Если условие if form.is_valid() ложно и данные не прошли валидацию -
        # передадим полученный объект в шаблон,
        # чтобы показать пользователю информацию об ошибке

        # Заодно заполним все поля формы данными, прошедшими валидацию,
        # чтобы не заставлять пользователя вносить их повторно
        return render(request, 'posts/create_post.html', {'form': form, 'is_edit': False})

    # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
    # пусть пользователь напишет что-нибудь
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form, 'is_edit': False})


def post_edit(request, id_post):
    post = Post.objects.get(id=id_post)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.pub_date = datetime.datetime.now()
            post.save()
            return redirect(f'/profile/{request.user.username}/')

        return render(request, 'posts/create_post.html', {'form': form, 'is_edit': True, 'post': post})

    form = PostForm(instance=post)


    return render(request, 'posts/create_post.html', {'form': form, 'is_edit': True, 'post': post, 'name': post.text})
