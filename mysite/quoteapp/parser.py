from bs4 import BeautifulSoup
from .models import Author, Quote, Tag
import requests
from django.contrib.auth.models import User


def parse_quotestoscrape():
    url = 'https://quotes.toscrape.com'
    current_page = '/'
    admin_user = User.objects.first()
    while current_page:
        response = requests.get(url + current_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        for q in quotes:
            quote = q.find('span', class_='text').text
            author_fullname = q.find('small', class_='author').text
            tags_list = [t.text for t in q.find_all('a', class_='tag')]
            
            if not Author.objects.filter(fullname=author_fullname).exists():
                about_page = q.find('a', string='(about)')['href']
                response_about = requests.get(url + about_page)
                soup_about = BeautifulSoup(response_about.text, 'html.parser')
                born_date = soup_about.find('span', class_="author-born-date").text
                born_location = soup_about.find('span', class_="author-born-location").text
                description = soup_about.find('div', class_="author-description").text.strip()
            else:
                born_date, born_location, description = '', '', ''
                
            author, _ = Author.objects.get_or_create(
                fullname=author_fullname,
                defaults={
                    'born_date': born_date,
                    'born_location': born_location,
                    'description': description,
                    'user': admin_user
                }
            )
            
            quote_obj_exists = Quote.objects.filter(author=author, quote=quote).exists()
            if not quote_obj_exists:
                new_quote = Quote.objects.create(
                    quote=quote,
                    author=author,
                    user=admin_user
                )
                
                for tag in tags_list:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag, defaults={'user': admin_user})
                    new_quote.tags.add(tag_obj)
          
        
        next_page = soup.find('li', class_='next')
        if next_page:
            current_page = next_page.find('a')['href']
        else:
            current_page = None