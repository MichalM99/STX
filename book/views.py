from datetime import datetime

import requests
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddBookForm, ImportBooksForm, SearchBookForm
from .models import Book
from .serializers import BookSerializer
from .utils import generate_api_link, get_results_from_api


class BookListApiView(APIView):
    """
    ApiView that allows filtering through query params like:
    title, author, date_from, date_to
    Example: ./api?date_from=2015-01-01&date_to=2019-01-01&title=Fresh
    """

    def get(self, request, *args, **kwargs):
        queryset = Book.objects.all()

        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)

        date_format = '%Y-%M-%d'
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        if date_from:
            date_from = datetime.strptime(date_from, date_format)
            queryset = queryset.filter(publication_date__gte=date_from)

        if date_to:
            date_to = datetime.strptime(date_to, date_format)
            queryset = queryset.filter(publication_date__lte=date_to)

        serializer = BookSerializer(queryset, many=True)

        return Response(serializer.data)


def book_list(request):
    """View that lists book."""
    search_form = SearchBookForm()
    results = []

    if 'title' in request.GET:
        search_form = SearchBookForm(request.GET)
        if search_form.is_valid():
            cd = search_form.cleaned_data
            title_query = cd['title']
            author_query = cd['author']
            lang_query = cd['language']
            date_from_query = cd['date_from'] if cd['date_from'] is not None else '1900-01-01'
            date_to_query = cd['date_to'] if cd['date_to'] is not None else '2100-01-01'
            results = Book.objects.filter(
                Q(title__icontains=title_query) & Q(author__icontains=author_query) & Q(
                    publication_lang__icontains=lang_query) & Q(publication_date__gte=date_from_query) & Q(
                    publication_date__lte=date_to_query)
            )
    else:
        results = Book.objects.all()

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    results = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'results': results, 'search_form': search_form})


def add_book(request):
    """View that allows adding book."""
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = AddBookForm()

    return render(request, 'add_book.html', {'form': form})


def edit_book(request, id):
    """View that allows editing book."""
    data = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        form = AddBookForm(instance=data, data=request.POST)
        if form.is_valid():
            form.save()
        return redirect("book_list")
    else:
        form = AddBookForm(instance=data)

    return render(request, 'add_book.html', {'form': form})


def import_books(request):
    """View that allows to import book from Google apis book"""
    if 'intitle' in request.GET:
        form = ImportBooksForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            link = generate_api_link(cd, 10)
            response = requests.get(link)
            results = get_results_from_api(response.json())
    else:
        results = []
        form = ImportBooksForm()

    return render(request, 'import_books.html', {'form': form, 'results': results})



