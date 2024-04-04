from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import transaction

from .models import Author, Quote, Tag

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup



def scrape_quotes(request=None):
    url = "http://quotes.toscrape.com"
    all_quotes = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            quote_text = quote.find("span", class_="text").text
            author_name = quote.find("small", class_="author").text.strip()

            all_quotes.append({'quote': quote_text, 'author': author_name})

        next_button = soup.find("li", class_="next")
        if next_button:
            url = urljoin(url, next_button.a['href'])
        else:
            url = None

    return all_quotes



def about_authors(request):
    url = "http://quotes.toscrape.com"
    all_authors = set()

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        authors = soup.find_all('small', class_='author')

        for author in authors:
            author_name = author.text.strip()
            author_url = urljoin(url, author.find_parent('div', class_='quote').a['href'])
            author_info = {
                'name': author_name,
                'url': author_url
            }
            all_authors.add((author_name, author_url))

        next_button = soup.find("li", class_="next")
        if next_button:
            url = urljoin(url, next_button.a['href'])
        else:
            url = None

    all_authors = [{'name': name, 'url': url} for name, url in all_authors]
    paginator = Paginator(all_authors, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'scrape_app/about_authors.html', {'page_obj': page_obj})


