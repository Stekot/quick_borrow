from django.contrib.auth import get_user_model

import pytest

from books.models import Author, Book

User = get_user_model()


@pytest.fixture
def author_fixture():
    return Author.objects.create(name="Sample Author")


@pytest.fixture
def book_fixture(author_fixture):
    return Book.objects.create(title="Sample Book", author=author_fixture)


@pytest.fixture
def user_fixture():
    return User.objects.create_user(email="testuser@example.com", password="testpass")
