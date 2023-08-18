from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin, FormView

from books.forms import BookLoanForm, BookReturnForm
from books.models import Book, BookLoan


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 9
    queryset = Book.objects.all().order_by('title').prefetch_related('book_loans')


class BookDetailView(FormView, DetailView):
    model = Book
    template_name = 'book_detail.html'
    lookup_field = 'uuid'
    form_class = BookLoanForm
    http_method_names = ['get', 'post']
    queryset = Book.objects.all().prefetch_related('book_loans', 'book_loans__user')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        book_loan = BookLoan.objects.get_or_create(book=self.object, user=request.user, return_datetime=None)[0]
        form = form_class(request.POST, instance=book_loan)
        redirect_to = self.get_success_url()
        if form.is_valid():
            # todo add message
            form.save()
        else:
            pass
            # todo error message
        return redirect(redirect_to)

    def get_success_url(self):
        return reverse('books:book_detail', kwargs={'uuid': self.object.uuid})

    def get_form_class(self):
        if self.object.is_available():
            return BookLoanForm
        return BookReturnForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(uuid=self.kwargs['uuid'])
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
