from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from django_filters.views import FilterMixin, FilterView

from books.filters import BookListFilter
from books.forms import BookLoanForm
from books.models import Book, BookLoan


class BookListView(FilterMixin, ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 9
    filterset_class = BookListFilter
    queryset = Book.objects.all().order_by("title").prefetch_related("book_loans")


class BookDetailView(FormView, DetailView):
    model = Book
    template_name = "book_detail.html"
    lookup_field = "uuid"
    form_class = BookLoanForm
    http_method_names = ["get", "post"]
    queryset = Book.objects.all().prefetch_related("book_loans", "book_loans__user")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        try:
            book_loan = BookLoan.objects.get(book=self.object, user=request.user, return_datetime=None)
        except BookLoan.DoesNotExist:
            book_loan = BookLoan(book=self.object, user=request.user)
        form = form_class(
            request.POST, instance=book_loan, initial={"action": book_loan.book.is_available() and "loan" or "return"}
        )
        redirect_to = self.get_success_url()
        if form.is_valid():
            form.save()
            messages.success(request, "Action completed successfully")
        else:
            for _field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
        return redirect(redirect_to)

    def get_success_url(self):
        return reverse("books:book_detail", kwargs={"uuid": self.object.uuid})

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(uuid=self.kwargs["uuid"])
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query") % {"verbose_name": queryset.model._meta.verbose_name}
            )
