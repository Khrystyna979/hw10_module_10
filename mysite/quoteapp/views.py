from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm, TagForm
from .models import Author, Quote, Tag
from django.db.models import Count
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
from .parser import parse_quotestoscrape

# Create your views here.
def main(request, page_number=1):
    quotes = Quote.objects.all()
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    paginator = Paginator(quotes, 10)
    page_obj = paginator.get_page(page_number)
    return render(request, 'quoteapp/quote_detail.html', context={'page_obj': page_obj, 'top_tags': top_tags})

def about(request, fullname):
    queryset = Author.objects.filter(fullname=fullname)
    author = get_object_or_404(queryset)
    return render(request, 'quoteapp/about.html', {'author': author})

def view_tag(request, tag, page_number=1):
    quotes_by_tag = Quote.objects.filter(tags__name__icontains=tag)
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    paginator = Paginator(quotes_by_tag, 10)
    page_obj = paginator.get_page(page_number)
    return render(request, 'quoteapp/tag_detail.html', context={'page_obj': page_obj, 'tag_name': tag, 'top_tags': top_tags})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_author.html', {'form': form})
            
    return render(request, 'quoteapp/add_author.html', {'form': AuthorForm()})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            form.save_m2m()
            return redirect(to='quoteapp:main')
    else:
        form = QuoteForm()
            
    return render(request, 'quoteapp/add_quote.html', {'form': form})

@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_tag.html', {'form': form})
        
    return render(request, 'quoteapp/add_tag.html', {'form': TagForm()})

@login_required
def scraping(request):
    if request.method == 'POST':
        parse_quotestoscrape()
        return redirect(to='quoteapp:main')
    
    return render(request, 'quoteapp/scraping.html')

@login_required
def view_my_quotes(request):
    quotes = Quote.objects.filter(user=request.user)
    return render(request, 'quoteapp/view_my_quotes.html', {'quotes': quotes})

@login_required
def view_my_tags(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'quoteapp/view_my_tags.html', {'tags': tags})

@login_required
def view_my_authors(request):
    authors = Author.objects.filter(user=request.user)
    return render(request, 'quoteapp/view_my_authors.html', {'authors': authors})

@login_required
def delete_author(request, fullname):
    author = get_object_or_404(Author, fullname=fullname, user=request.user)
    if request.method =="POST":
        author.delete()
        return redirect(to='quoteapp:my-authors')
    
    context = {
        'object_name': author.fullname,
        'warning_message': '❗️ Deleting this author will also delete all their quotes! This action cannot be undone ❗️',
        'cancel_url': 'quoteapp:my-authors'
    }
    
    return render(request, 'quoteapp/delete.html', context)

@login_required
def delete_tag(request, tag):
    tag = get_object_or_404(Tag, name=tag, user=request.user)
    if request.method =="POST":
        tag.delete()
        return redirect(to='quoteapp:my-tags')
    
    context = {
        'object_name': tag.name,
        'warning_message': '❗️ Deleting this tag cannot be undone ❗️ ',
        'cancel_url': 'quoteapp:my-tags'
    }
    
    return render(request, 'quoteapp/delete.html', context)

@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id, user=request.user)
    if request.method =="POST":
        quote.delete()
        return redirect(to='quoteapp:my-quotes')
    
    context = {
        'object_name': f'Quote "{quote.quote[:30]}...',
        'warning_message': '❗️ Deleting this quote cannot be undone ❗️ ',
        'cancel_url': 'quoteapp:my-quotes'
    }
    
    return render(request, 'quoteapp/delete.html', context)