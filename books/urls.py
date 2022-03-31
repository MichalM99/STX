from django.urls import path

from books import views
from books.views import BookListApiView

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book//<int:id>/', views.edit_book, name='edit_book'),
    path('import_books/', views.import_books, name='import_books'),
    path('api', BookListApiView.as_view(), name='api_view'),
]
