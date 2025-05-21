from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = 'app'

urlpatterns = [
    path('',            views.index,        name='index'),
    path('about/',      views.about,        name='about'),
    path('contact/',    views.contact,      name='contact'),
    path('feedback/',   views.pool,         name='feedback'),
    path('registration/', views.registration, name='registration'),

    path('login/',  auth_views.LoginView.as_view(
                        template_name     = 'app/login.html',
                        authentication_form = LoginForm
                   ),
                   name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Пути для блога
    path('blog/',          views.blog_list,    name='blog_list'),
    path('blog/add/',      views.blog_create,  name='blog_create'),   # ← новинка
    path('blog/<int:pk>/', views.blog_detail,  name='blog_detail'),
]
