from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.conf import settings

from .forms import FeedbackForm, BlogForm, CommentForm
from .models import Blog, Comment

def index(request):
    assert isinstance(request, HttpRequest)
    return render(request,'app/index.html',{
        'title':   'Главная',
        'message': 'Здесь рождается счастье!',
        'year':    datetime.now().year,
    })

def about(request):
    assert isinstance(request, HttpRequest)
    return render(request,'app/about.html',{
        'title':   'О нас',
        'message': 'Описание нашего перинатального центра, его миссии и ценностей.',
        'year':    datetime.now().year,
    })

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(request,'app/contact.html',{
        'title':   'Контакты',
        'message': 'Если у вас есть вопросы — свяжитесь с нами любым удобным способом.',
        'year':    datetime.now().year,
    })

def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            data = {
                'name':             cd['name'],
                'email':            cd['email'],
                'rating':           dict(form.fields['rating'].choices)[cd['rating']],
                'favorite_section': dict(form.fields['favorite_section'].choices)[cd['favorite_section']],
                'subscribe':        'Да' if cd['subscribe'] else 'Нет',
                'comments':         cd['comments'],
            }
            form = None
    else:
        form = FeedbackForm()
    return render(request,'app/pool.html',{
        'title':'Обратная связь',
        'year': datetime.now().year,
        'form': form,
        'data': data,
    })

def registration(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите, пожалуйста.')
            return redirect('app:login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserCreationForm()
    return render(request,'app/registration.html',{
        'regform': form,
        'year':    datetime.now().year,
    })

def blog_list(request):
    posts = Blog.objects.all()
    return render(request, 'app/blog_list.html', {
        'title': 'Блог',
        'posts': posts,
        'year':  datetime.now().year,
    })

@user_passes_test(lambda u: u.is_superuser)
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = BlogForm()
    return render(request, 'app/blog_form.html', {
        'title': 'Добавить статью',
        'form':  form,
        'year':  datetime.now().year,
    })

def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    # Обработка отправки формы комментариев
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('app:login')}?next={request.path}")
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    # Получаем все комментарии к статье
    comments = post.comments.all()

    return render(request, 'app/blog_detail.html', {
        'title': post.title,
        'post':  post,
        'year':  datetime.now().year,
        'comment_form': comment_form,
        'comments': comments,
    })
def video_list(request):
    """
    Страница «Видео материалы» — просто два <video>-плеера,
    берущие файлы из папки media/videos/.
    """
    return render(request, 'app/videos.html', {
        'title': 'Видео материалы',
        # Пути к двум видео:
        'videos': [
            settings.MEDIA_URL + 'videos/video1.mp4',
            settings.MEDIA_URL + 'videos/video2.mp4',
        ]
    })
