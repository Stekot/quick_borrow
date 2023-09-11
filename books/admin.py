from django.contrib import admin

from books.models import Author, Book, BookLoan


class BookLoanInline(admin.TabularInline):
    model = BookLoan
    fields = ("book", "user", "loan_datetime", "return_datetime")
    ordering = ("-loan_datetime",)
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
    )
    search_fields = (
        "title",
        "author__name",
    )
    list_filter = (
        "author",
        "isbn",
    )
    ordering = ("title",)
    inlines = [BookLoanInline]


class BookInline(admin.TabularInline):
    model = Book
    fields = (
        "title",
        "isbn",
    )
    ordering = ("title",)
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "book_count",
    )
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [BookInline]
