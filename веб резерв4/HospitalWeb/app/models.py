from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse

# импорт User для связи «многие к одному»
from django.contrib.auth.models import User

class Blog(models.Model):
    title   = models.CharField('Заголовок', max_length=200)
    summary = models.TextField('Краткое содержание', max_length=500)
    content = models.TextField('Полное содержание')
    posted  = models.DateTimeField('Опубликована', default=datetime.now, db_index=True)

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

# Регистрация модели Блога
admin.site.register(Blog)


# --- НОВАЯ МОДЕЛЬ КОММЕНТАРИЕВ ---
class Comment(models.Model):
    content = models.TextField('Текст комментария')
    created = models.DateTimeField('Дата комментария', auto_now_add=True, db_index=True)
    author  = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    post    = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья'
    )

    def __str__(self):
        return f'Комментарий {self.pk} к "{self.post.title}"'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created']

# Регистрация модели Комментариев
admin.site.register(Comment)
