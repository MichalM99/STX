import pytest
from django.test import TestCase
from django.urls import reverse

from factories import BookFactory


@pytest.mark.django_db
class TestBookListView(TestCase):
    """Test cases for book_list view."""

    def setUp(self):
        factory = BookFactory.create_batch(15)

    def test_url_existance(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(len(response.context['results']), 10)

    def test_correct_template(self):
        response = self.client.get(reverse('book_list'))
        self.assertTemplateUsed(response, 'book_list.html')


@pytest.mark.django_db
class TestAddBookView(TestCase):
    """Test cases for add_book view."""

    def test_url_existance(self):
        response = self.client.get('/add_book/')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('add_book'))
        self.assertTemplateUsed(response, 'add_book.html')


@pytest.mark.django_db
class TestEditBookView(TestCase):
    """Test cases for edit_book view."""

    def setUp(self):
        self.factory = BookFactory()

    def test_url_existance(self):
        response = self.client.get('/edit_book/{}/'.format(self.factory.pk))
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        response = self.client.get(reverse('edit_book', kwargs={'id': self.factory.pk}))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('edit_book', kwargs={'id': self.factory.pk}))
        self.assertTemplateUsed(response, 'add_book.html')


class TestImportBookView(TestCase):
    """Test cases for import_books view."""

    def test_url_existance(self):
        response = self.client.get('/import_books/')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        response = self.client.get(reverse('import_books'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('import_books'))
        self.assertTemplateUsed(response, 'import_books.html')


class TestBookListApiView(TestCase):
    """Test cases for BookListApiView."""

    def setUp(self):
        factory = BookFactory()

    def test_url_existance(self):
        response = self.client.get('/api')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        response = self.client.get(reverse('api_view'))
        self.assertEqual(response.status_code, 200)

    def test_collection(self):
        response = self.client.get(reverse('api_view'), format='json')
        self.assertEqual(len(response.data), 1)

    def test_get_query_params(self):
        BookFactory(title='Example', author='ExampleAuthor')
        response = self.client.get('/api?title=Example')
        title = response.data[0]['title']
        author = response.data[0]['author']
        self.assertEqual(title, 'Example')
        self.assertEqual(author, 'ExampleAuthor')
