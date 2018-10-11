from django.db import models


class Article(models.Model):
    m_ID = models.CharField(max_length=50, primary_key=True)
    m_url = models.CharField(max_length=200)
    m_title = models.CharField(max_length=200)
    m_time = models.DateTimeField()
    m_content = models.TextField()

    def __str__(self):
        return self.m_title

class Word(models.Model):
    m_word = models.CharField(max_length=200, primary_key=True)
    m_article = models.ManyToManyField(Article)

    def __str__(self):
        return self.m_word

    def article_list(self):
        return ','.join(i.m_title for i in self.m_article.all())