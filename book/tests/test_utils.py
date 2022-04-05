import unittest

import pytest
import requests

from book.models import Book
from book.utils import create_book_obj, generate_api_link, get_results_from_api


class TestUtils(unittest.TestCase):
    """Test cases for book.utils."""

    @pytest.mark.django_db
    def test_create_book_obj(self):
        book = {
            'title': 'Book title 0',
            'author': 'Author name 0',
            'publication_date': '2022-02-02',
            'isbn': '1234567890123',
            'number_of_pages': 50,
            'cover_url': 'http://127.0.0.1:8000/',
            'publication_lang': 'Polish',
        }
        create_book_obj(book, 'http://127.0.0.1:8000/')

        created_object = Book.objects.last().__dict__
        del created_object['_state']
        del created_object['id']
        created_object['publication_date'] = '2022-02-02'

        self.assertEqual(created_object, book)
        self.assertEqual(Book.objects.count(), 1)

    def test_generate_api_link(self):
        cd = {
            'intitle': 'test',
            'inauthor': 'test',
            'inpublisher': 'test',
            'subject': 'test',
            'isbn': 'test',
            'lccn': 'test',
            'oclc': 'test'
        }
        test_link = 'https://www.googleapis.com/books/v1/' \
                    'volumes?q=+intitle:test+inauthor:test+' \
                    'inpublisher:test+subject:test+isbn:test+' \
                    'lccn:test+oclc:test&maxResults=10'
        link = generate_api_link(cd, 10)

        self.assertEqual(link, test_link)

    @pytest.mark.django_db
    def test_get_results_from_api(self):
        test_link = 'https://www.googleapis.com/books/v1/volumes?q=+intitle:test&maxResults=1'

        response = requests.get(test_link)
        test_results = [{'title': 'Test Marshmallow', 'author': ['Walter Mischel'], 'publication_date': '2015-01',
                         'isbn': '8364846116', 'number_of_pages': 320, 'cover_url': "<a href=''>Link</a>",
                         'publication_lang': 'pl'}]

        results = get_results_from_api(response.json())

        self.assertEqual(results, test_results)
