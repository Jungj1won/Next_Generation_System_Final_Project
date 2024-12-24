from django.db import models

class Article(models.Model):
    index = models.CharField(max_length=100, primary_key=True)  # index를 기본 키로 설정
    link = models.CharField(max_length=200)
    doi = models.CharField(max_length=100, null=True)
    subject1 = models.CharField(max_length=50)
    subject2 = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    abstract = models.TextField()
    date = models.CharField(max_length=200)
    etc = models.TextField(null=True)

    class Meta:
        db_table = 'ARTICLE'
