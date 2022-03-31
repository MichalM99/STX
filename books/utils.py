from books.models import Book


def create_book_obj(book, cover_url):
    """Function creates Book obj based on dict."""
    if not Book.objects.filter(isbn=book['isbn']):
        Book.objects.create(
            title=book['title'],
            author=book['author'],
            publication_date=book['publication_date'],
            isbn=book['isbn'],
            number_of_pages=book['number_of_pages'],
            cover_url=cover_url,
            publication_lang=book['publication_lang']
        )


def generate_api_link(cd, max_results):
    """Function generates correct API link with query params."""
    link = f"https://www.googleapis.com/books/v1/volumes?q="
    for key, item in cd.items():
        if item is not '':
            link += f"+{key}:{item}"
    link += f"&maxResults={max_results}"
    return link


def get_results_from_api(response):
    """Function that returns data from api correctly formatted."""
    results = []
    data = response.json()
    if data['totalItems'] > 0:
        for item in data['items']:
            cover_url = item['volumeInfo']['imageLinks']['thumbnail'] \
                if 'imageLinks' in item['volumeInfo'] else ""
            book = {
                'title': item['volumeInfo']['title'],
                'author': item['volumeInfo']['authors'] \
                    if 'authors' in item['volumeInfo'] else "",
                'publication_date': item['volumeInfo']['publishedDate'] \
                    if 'publishedDate' in item['volumeInfo'] else "2021-01-01",
                'isbn': item['volumeInfo']['industryIdentifiers'][0]['identifier'] \
                    if 'industryIdentifiers' in item['volumeInfo'] else "",
                'number_of_pages': item['volumeInfo']['pageCount'] \
                    if 'pageCount' in item['volumeInfo'] else 0,
                'cover_url': "<a href='{}'>Link</a>".format(cover_url),
                'publication_lang': item['volumeInfo']['language'],
            }
            results.append(book)
            create_book_obj(book, cover_url)
    return results