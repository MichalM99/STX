from django.core.validators import MaxValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    author = models.CharField(max_length=255, verbose_name='Author')
    publication_date = models.CharField(max_length=11, verbose_name='Publication date')
    isbn = models.CharField(max_length=13, verbose_name='ISBN')
    number_of_pages = models.IntegerField(validators=[MaxValueValidator(99999)], verbose_name='Number of pages')
    cover_url = models.URLField(verbose_name='Cover url')
    publication_lang = models.CharField(max_length=255, verbose_name='Publication language')

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']

    def __str__(self):
        return self.title + ' ' + self.author





