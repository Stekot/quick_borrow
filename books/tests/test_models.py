from django.contrib.auth import get_user_model

import pytest

from books.models import Author, Book, BookLoan

User = get_user_model()


@pytest.mark.django_db
def test_author_book_count(author_fixture, book_fixture, user_fixture):
    Book.objects.create(title="Sample Book 2", author=author_fixture)

    assert author_fixture.book_count() == 2


@pytest.mark.django_db
def test_book_is_available(author_fixture, book_fixture, user_fixture):
    assert book_fixture.is_available

    BookLoan.objects.create(book=book_fixture, user=user_fixture)

    assert not book_fixture.is_available()
