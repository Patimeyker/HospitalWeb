from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse

# импортим User для связи «многие к одной»
from django.contrib.auth.models import User

class Blog(models.Model):
    title   = models.CharField('Заголовок', max_length=200)
    summary = models.TextField('Краткое содержание', max_length=500)
    content = models.TextField('Полное содержание')
    posted  = models.DateTimeField('Опубликована', default=datetime.now, db_index=True)

    # Новое поле — связь с моделью User
    author = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Автор"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app:blog_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'
        ordering = ['-posted']

# Регистрация в админке — здесь ничего не меняется
admin.site.register(Blog)
