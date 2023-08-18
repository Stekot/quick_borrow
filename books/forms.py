from django import forms
from django.utils import timezone

from books.models import BookLoan


class BookLoanForm(forms.ModelForm):

    ACTION_FIELD_VALUE = 'loan'
    action = forms.CharField(widget=forms.HiddenInput(), initial=ACTION_FIELD_VALUE)

    class Meta:
        model = BookLoan
        fields = ['action']

    def clean(self):
        super().clean()
        book = self.instance.book
        action = self.cleaned_data['action']
        if not book.is_available():
            raise forms.ValidationError('Book is not available for loan')
        if action != self.ACTION_FIELD_VALUE:
            raise forms.ValidationError('Invalid action')
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.loan_datetime = self.instance.loan_datetime or timezone.now()
        self.instance.return_datetime = None
        return super().save(commit)


class BookReturnForm(forms.ModelForm):

    ACTION_FIELD_VALUE = 'return'
    action = forms.CharField(widget=forms.HiddenInput(), initial=ACTION_FIELD_VALUE)

    class Meta:
        model = BookLoan
        fields = ['action']

    def clean(self):
        super().clean()
        book = self.instance.book
        action = self.cleaned_data['action']
        if book.is_available():
            raise forms.ValidationError('Book is already returned')
        if action != self.ACTION_FIELD_VALUE:
            raise forms.ValidationError('Invalid action')
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.return_datetime = timezone.now()
        return super().save(commit)
