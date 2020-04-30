from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.http import HttpResponse
from . import models

BASE_CRAIGSLIST_URL = 'https://malaysia.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # Getting the webpage, creating a response object.
    response = requests.get(final_url)
    # Extracting the source code of the page
    data = response.text
    # parse html to soup variable
    soup = BeautifulSoup(data, features='html.parser')
    # To get the number of result searched

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_posting = []
    image_id = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        # If images found
        if post.find(class_='result-image').get('data-ids'):
            retrive_id = post.find(class_='result-image').get('data-ids')
            post_image_id = retrive_id.split(',')
            post_image = BASE_IMAGE_URL.format(post_image_id[0][2:])
            print(post_image)

        # if no image found
        else:
            post_image = "https://www.indiaspora.org/wp-content/uploads/2018/10/image-not-available.jpg"

        final_posting.append((post_title, post_url, post_price, post_image))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_posting,

    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)