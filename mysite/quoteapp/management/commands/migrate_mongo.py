import os
from dotenv import load_dotenv
from mongoengine import connect
from mongoengine.connection import get_db
from django.core.management.base import BaseCommand
from quoteapp.models import Author, Tag, Quote
from django.contrib.auth.models import User

load_dotenv()

MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DOMAIN = os.environ.get('DOMAIN')

connect(host=f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{DOMAIN}/{DB_NAME}?appName=Cluster0", ssl=True)

# Джанго обов'язково шукає саме цей клас
class Command(BaseCommand):

    def handle(self, *args, **options):
        db = get_db()
        
        authors_collection = db['authors']
        quotes_collection = db['quotes']
        
        all_mongo_authors = authors_collection.find()
        all_mongo_quotes = quotes_collection.find()
        
        admin_user = User.objects.first()
        
        for item in all_mongo_authors:
            author, _ = Author.objects.get_or_create(
                fullname=item['fullname'],
                born_date=item['born_date'],
                born_location=item['born_location'],
                description=item['description'],
                user=admin_user
            )
            
        for item in all_mongo_quotes:
            author_id = item['author']
            author_document = authors_collection.find_one({'_id': author_id})
            
            if author_document:
                author_name = author_document['fullname']
                django_author = Author.objects.filter(fullname=author_name).first()
            
                if django_author:
                    quote, _ = Quote.objects.get_or_create(
                        quote=item['quote'],
                        author=django_author,
                        user=admin_user
                    )
    
                    for tag_name in item['tags']:
                        django_tag, _ = Tag.objects.get_or_create(name=tag_name)
                        quote.tags.add(django_tag)