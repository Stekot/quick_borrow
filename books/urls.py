from django.urls import path

from books.views import BookDetailView, BookListView

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<uuid:uuid>", BookDetailView.as_view(), name="book_detail"),
]
