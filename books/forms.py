from django import forms
from django.utils import timezone

from books.models import BookLoan


class BookLoanForm(forms.ModelForm):
    LOAN_ACTION = "loan"
    RETURN_ACTION = "return"

    action = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = BookLoan
        fields = ["action"]

    def clean(self):
        super().clean()
        if self.cleaned_data["action"] == self.LOAN_ACTION:
            return self._clean_loan_action()
        elif self.cleaned_data["action"] == self.RETURN_ACTION:
            return self._clean_return_action()
        else:
            raise forms.ValidationError("Invalid action")

    def _clean_loan_action(self):
        if not self.instance.book.is_available():
            raise forms.ValidationError("Book is not available for a loan")
        return self.cleaned_data

    def _clean_return_action(self):
        if self.instance.book.is_available():
            raise forms.ValidationError("Book is already returned")
        return self.cleaned_data

    def save(self, commit=True):
        if self.cleaned_data["action"] == self.LOAN_ACTION:
            self._save_loan_action()
        if self.cleaned_data["action"] == self.RETURN_ACTION:
            self._save_return_action()
        return super().save(commit)

    def _save_loan_action(self):
        self.instance.loan_datetime = self.instance.loan_datetime or timezone.now()
        self.instance.return_datetime = None

    def _save_return_action(self):
        self.instance.return_datetime = timezone.now()
