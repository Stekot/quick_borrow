from django.contrib import admin

from books.models import Author, Book


class BookLoanInline(admin.TabularInline):
    model = 'books.BookLoan'
    list_display = ('book', 'user__full_name', 'user__email', 'loan_datetime', 'return_datetime')
    ordering = ('-loan_datetime',)
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    search_fields = ('title', 'author',)
    list_filter = ('author', 'isbn',)
    ordering = ('title',)
    tabular_inlines = [BookLoanInline]


class BookInline(admin.TabularInline):
    model = 'books.Book'
    list_display = ('title', 'isbn',)
    ordering = ('title',)
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count',)
    search_fields = ('name',)
    ordering = ('name',)
    tabular_inlines = [BookInline]