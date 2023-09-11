from django.contrib.auth import get_user_model
from django.utils import timezone

import pytest

from books.forms import BookLoanForm
from books.models import BookLoan

User = get_user_model()


@pytest.mark.django_db
def test_book_loan_valid(author_fixture, book_fixture, user_fixture):
    data = {"action": "loan"}
    form = BookLoanForm(data, instance=BookLoan(book=book_fixture, user=user_fixture))
    assert form.is_valid()


@pytest.mark.django_db
def test_book_loan_form_invalid_action(author_fixture, book_fixture, user_fixture):
    data = {"action": "invalid_action"}
    form = BookLoanForm(data, instance=BookLoan(book=book_fixture, user=user_fixture))
    assert not form.is_valid()


@pytest.mark.django_db
def test_book_return_form_valid(author_fixture, book_fixture, user_fixture):
    book_loan = BookLoan.objects.create(book=book_fixture, user=user_fixture)
    data = {"action": "return"}
    form = BookLoanForm(data, instance=book_loan)
    assert form.is_valid()


@pytest.mark.django_db
def test_book_return_form_invalid_action(author_fixture, book_fixture, user_fixture):
    book_loan = BookLoan.objects.create(book=book_fixture, user=user_fixture)
    data = {"action": "invalid_action"}
    form = BookLoanForm(data, instance=book_loan)
    assert not form.is_valid()


@pytest.mark.django_db
def test_book_loan_form_already_loaned(author_fixture, book_fixture, user_fixture):
    _ = BookLoan.objects.create(book=book_fixture, user=user_fixture)  # Loan the book
    data = {"action": "loan"}
    form = BookLoanForm(data, instance=BookLoan(book=book_fixture, user=user_fixture))
    assert not form.is_valid()


@pytest.mark.django_db
def test_book_return_form_not_loaned(author_fixture, book_fixture):
    data = {"action": "return"}
    form = BookLoanForm(data, instance=BookLoan(book=book_fixture))
    assert not form.is_valid()


@pytest.mark.django_db
def test_book_return_form_twice(author_fixture, book_fixture, user_fixture):
    book_loan = BookLoan.objects.create(book=book_fixture, user=user_fixture)
    book_loan.return_datetime = timezone.now()
    book_loan.save()  # Return the book
    data = {"action": "return"}
    form = BookLoanForm(data, instance=book_loan)
    assert not form.is_valid()
