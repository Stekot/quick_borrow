import uuid as uuid

from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def book_count(self):
        return self.books.count()

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    goodreads_id = models.CharField(max_length=100, blank=True, null=True, editable=False, db_index=True)

    def is_available(self):
        return not self.book_loans.filter(return_datetime__isnull=True).exists()

    def __str__(self):
        return self.title


class BookLoan(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_loans')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='book_loans')
    loan_datetime = models.DateTimeField(auto_now_add=True)  # todo change name to reflect datatype
    return_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.book} - {self.user}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
