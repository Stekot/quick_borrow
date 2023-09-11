from django.db.models import Q

import django_filters

from books.models import Book


class BookListFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value) | Q(author__name__icontains=value)
        )

    class Meta:
        model = Book
        fields = ["search"]
