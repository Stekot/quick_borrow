import uuid as uuid_module

from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid_module.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def book_count(self) -> int:
        return self.books.count()

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid_module.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)
    isbn = models.CharField(max_length=13, default="", blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    goodreads_id = models.CharField(max_length=100, blank=True, null=True, editable=False, db_index=True)  # noqa: DJ01

    def is_available(self) -> bool:
        return not self.book_loans.filter(return_datetime__isnull=True).exists()

    def __str__(self) -> str:
        return self.title


class BookLoan(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid_module.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_loans")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="book_loans")
    loan_datetime = models.DateTimeField(auto_now_add=True)
    return_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.book} - {self.user}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
