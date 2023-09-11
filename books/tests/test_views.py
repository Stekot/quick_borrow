from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest

from books.forms import BookLoanForm
from books.models import Author, Book, BookLoan

User = get_user_model()


# Tests for BookListView
@pytest.mark.django_db
def test_book_list_view(client, author_fixture, book_fixture):
    url = reverse("books:book_list")
    response = client.get(url)
    assert response.status_code == 200
    assert "book_list" in response.context
    assert book_fixture.title in response.content.decode()  # Check if book title is in the content


@pytest.mark.django_db
def test_book_list_view_filtering(client, author_fixture):
    book1 = Book.objects.create(title="Book One", author=author_fixture)
    book2 = Book.objects.create(title="Book Two", author=author_fixture)

    url = reverse("books:book_list") + "?search=One"
    response = client.get(url)
    assert response.status_code == 200
    assert book1.title in response.content.decode()
    assert book2.title not in response.content.decode()


@pytest.mark.django_db
def test_book_list_view_filter_by_author_name(client, author_fixture):
    author2 = Author.objects.create(name="Jane Doe")
    book1 = Book.objects.create(title="Book One", author=author_fixture)
    book2 = Book.objects.create(title="Book Two", author=author2)

    url = reverse("books:book_list") + "?search=Jane"
    response = client.get(url)
    assert response.status_code == 200
    assert book1.title not in response.content.decode()
    assert book2.title in response.content.decode()


@pytest.mark.django_db
def test_book_detail_view(client, author_fixture, book_fixture):
    url = reverse("books:book_detail", kwargs={"uuid": book_fixture.uuid})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["book"] == book_fixture
    assert book_fixture.title in response.content.decode()  # Check if book title is in the content


@pytest.mark.django_db
def test_book_detail_view_invalid_uuid(client, author_fixture, book_fixture):
    url = reverse("books:book_detail", kwargs={"uuid": "12345678-1234-5678-1234-567812345678"})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_book_list_view_filtering(client, author_fixture):
    book1 = Book.objects.create(title="Book One", author=author_fixture)
    book2 = Book.objects.create(title="Book Two", author=author_fixture)
    book3 = Book.objects.create(title="Book Three", author=author_fixture)

    url = reverse("books:book_list") + "?search=One"
    response = client.get(url)
    assert response.status_code == 200
    assert book1.title in response.content.decode()
    assert book2.title not in response.content.decode()
    assert book3.title not in response.content.decode()


@pytest.mark.django_db
def test_book_list_view_filter_by_author_name(client, author_fixture):
    author2 = Author.objects.create(name="Jane Doe")
    book1 = Book.objects.create(title="Book One", author=author_fixture)
    book2 = Book.objects.create(title="Book Two", author=author2)
    book3 = Book.objects.create(title="Book Three", author=author2)

    url = reverse("books:book_list") + "?search=Jane"
    response = client.get(url)
    assert response.status_code == 200
    assert book1.title not in response.content.decode()
    assert book2.title in response.content.decode()
    assert book3.title in response.content.decode()


@pytest.mark.django_db
def test_loan_book(client, author_fixture, book_fixture, user_fixture):
    client.force_login(user_fixture)
    assert book_fixture.is_available()

    url = reverse("books:book_detail", kwargs={"uuid": book_fixture.uuid})
    post_data = {
        "action": BookLoanForm.LOAN_ACTION,
    }
    response = client.post(url, post_data)
    assert response.status_code == 302
    assert not book_fixture.is_available()


@pytest.mark.django_db
def test_return_book(client, author_fixture, book_fixture, user_fixture):
    BookLoan.objects.create(book=book_fixture, user=user_fixture, return_datetime=None)
    client.force_login(user_fixture)
    assert not book_fixture.is_available()

    url = reverse("books:book_detail", kwargs={"uuid": book_fixture.uuid})
    post_data = {
        "action": BookLoanForm.RETURN_ACTION,
    }
    response = client.post(url, post_data)

    assert response.status_code == 302
    book_fixture.refresh_from_db()
    assert book_fixture.is_available()
