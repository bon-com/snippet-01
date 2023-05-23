from django.db import models
from django.conf import settings
from .consts import SNIPPET_CAG

# Create your models here.
class Snippet(models.Model):
    title = models.CharField('タイトル', max_length=128) # スニペット の タイトル 
    code = models.TextField('コード', blank=True) # ソースコード
    description = models.TextField('説明', blank=True) # コードの解説文（文字制限なし）
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', on_delete = models.CASCADE) # ユーザーモデルの主キー
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    category = models.CharField(
        'カテゴリ',
        max_length=100,
        choices=SNIPPET_CAG,
        blank=True
    )

    class Meta:
        db_table = 'snippets'
        verbose_name = 'スニペット'
        verbose_name_plural = "スニペット"

    def __str__(self):
        return self.title

class Comment(models.Model):
    title = models.CharField('タイトル', max_length=128, blank=True) 
    code = models.TextField('コード', blank=True) # ソースコード
    text = models.TextField('コメント', blank=False)
    commented_at = models.DateTimeField('投稿日', auto_now_add=True)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', on_delete=models.CASCADE)
    commented_to = models.ForeignKey(Snippet, verbose_name='スニペット', on_delete=models.CASCADE)
    category = models.CharField(
        'カテゴリ',
        max_length=100,
        choices=SNIPPET_CAG,
        blank=True
    )
    class Meta:
        db_table = 'comments'
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'

    def __str__(self):
        return self.title