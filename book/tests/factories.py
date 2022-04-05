import string

import factory
import factory.fuzzy

from book.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda x: f"Book title {x}")
    author = factory.Sequence(lambda x: f"Author name {x}")
    publication_date = factory.Faker('date_object')
    isbn = factory.fuzzy.FuzzyText(length=13, chars=string.digits)
    number_of_pages = factory.fuzzy.FuzzyInteger(50, 999)
    cover_url = str(factory.fuzzy.FuzzyText(length='12',
                                        prefix='https://www.',
                                        suffix='.com'))
    publication_lang = factory.fuzzy.FuzzyChoice(['Polish', 'English', 'Spanish'])