from django.contrib import admin
from .models import Article,Word
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['m_ID','m_url','m_title','m_time','m_content']
admin.site.register(Article,ArticleAdmin)

class WordAdmin(admin.ModelAdmin):
    list_display = ['m_word','article_list']
admin.site.register(Word,WordAdmin)