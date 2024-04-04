from django.forms import ModelForm, CharField, DateField, Textarea, TextInput, ModelChoiceField
from django import forms
from .models import Author, Quote

class ScrapeForm(forms.Form):
    url = forms.URLField(label='URL', initial='https://quotes.toscrape.com')


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, required=True)
    born_date = DateField(required=False)
    born_location = CharField(max_length=50, required=False)
    description = CharField(max_length=150)

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class QuoteForm(ModelForm):

    author = ModelChoiceField(queryset=Author.objects.all(), label='Author', required=True)
    tags = forms.CharField(label='Tags', max_length=100, required=False)
    quote = forms.CharField(label='Quote', max_length=500, required=True)

    class Meta:
        model = Quote
        fields = ['author', 'tags', 'quote']


    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get('author')

        if not author:
            raise forms.ValidationError('Author name is required.')

        author, created = Author.objects.get_or_create(fullname=author)
        cleaned_data['author'] = author

        return cleaned_data