import unittest
from datetime import datetime

import pytest
from factories import BookFactory


class TestBookModel(unittest.TestCase):
    """Test cases for Book model."""

    @classmethod
    def setUp(self):
        self.factory = BookFactory()

    @pytest.mark.django_db
    def test_attrs(self):
        self.assertEqual(self.factory.title, 'Book title 0')
        self.assertEqual(self.factory.author, 'Author name 0')
        self.assertEqual(bool(datetime.strptime(str(self.factory.publication_date), '%Y-%m-%d')), True)
        self.assertEqual(len(self.factory.isbn), 13)
        self.assertEqual(str(self.factory.number_of_pages).isdigit(), True)
        self.assertEqual(self.factory.publication_lang in ['Polish', 'Spanish', 'English'], True)

    @pytest.mark.django_db
    def test_verbose_names(self):
        verbose = self.factory._meta.verbose_name
        verbose_plural = self.factory._meta.verbose_name_plural

        self.assertEqual(verbose, 'Book')
        self.assertEqual(verbose_plural, 'Books')

    @pytest.mark.django_db
    def test_str_override(self):
        obj_str = str(self.factory)
        test_str = 'Book title 1 Author name 1'

        self.assertEqual(obj_str, test_str)
