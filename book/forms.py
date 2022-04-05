from django import forms
from django.forms import DateInput

from .models import Book


class SearchBookForm(forms.Form):
    """Form for Book search bar."""
    title = forms.CharField(label='Title', required=False)
    author = forms.CharField(label='Author', required=False)
    language = forms.CharField(label='Language', required=False)
    date_from = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                label='Publication date from', required=False)
    date_to = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                              label='Publication date to', required=False)


class AddBookForm(forms.ModelForm):
    """Form for adding Book."""
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'publication_date': DateInput(attrs={'type': 'date'}),
        }


class ImportBooksForm(forms.Form):
    """Form that serves for importing book."""
    intitle = forms.CharField(label='Title', required=False)
    inauthor = forms.CharField(label='Author', required=False)
    inpublisher = forms.CharField(label='Publisher', required=False)
    subject = forms.CharField(label='Subject', required=False)
    isbn = forms.CharField(label='ISBN', required=False)
    lccn = forms.CharField(label='LCCN', required=False)
    oclc = forms.CharField(label='OCLC', required=False)




