from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag
from .utils import scrape_quotes

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data.get('fullname')
            existing_author = Author.objects.filter(fullname=author_name).first()
            if not existing_author:
                author = form.save(commit=False)
                author.user = request.user
                author.save()
                author_id=author.pk
                return redirect(reverse('scrape_app:author_detail', kwargs={'author_id': author_id}))
            else:
                messages.error(request, 'Author already exists.')
    else:
         form = AuthorForm()
    return render(request, 'scrape_app/add_author.html', {'form': form})

def author_detail(request, author_id):
    author = Author.objects.get(pk=author_id)
    return render(request, 'scrape_app/author_detail.html', {'author': author})

def authors_list_db(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, 'scrape_app/authors_list_db.html', context)


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():

            quote = form.save(commit=False)
            quote.user = request.user
            author_name = form.cleaned_data.get('author')

            quote.save()

            tags_input = form.cleaned_data.get('tags')
            if tags_input:
                tags_list = [tag.strip() for tag in tags_input.split(',')]
                for tag_name in tags_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    quote.tags.add(tag)
            quote_id = quote.pk
            return redirect(reverse('scrape_app:quote_detail', kwargs={'quote_id': quote_id}))
    else:
        form = QuoteForm()
    return render(request, 'scrape_app/add_quote.html', {'form': form})

def quote_detail(request, quote_id):
    quote = Quote.objects.get(pk=quote_id)
    return render(request, 'scrape_app/quote_detail.html', {'quote': quote})

def quotes_list_db(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "scrape_app/quotes_list_db.html", context)


def quotes_www(request):
    quotes_data = scrape_quotes()

    for quote_data in quotes_data:
        author_name = quote_data['author']
        quote_text = quote_data['quote']

        author, _ = Author.objects.get_or_create(fullname=author_name)
        quote = Quote(quote=quote_text, author=author)
        quote.save()

    quotes = Quote.objects.all()

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'scrape_app/quotes_www.html', {'page_obj': page_obj})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})

def quotes_by_tag(request, tag):
    try:
        tag = Tag.objects.get(name=tag)
        quotes = Quote.objects.filter(tags=tag)
        context = {
            'tag': tag,
            'quotes': quotes,
        }
        return render(request, 'scrape_app/quotes_by_tag.html', context)
    except Tag.DoesNotExist:
        return render(request, 'scrape_app/tag_not_found.html')