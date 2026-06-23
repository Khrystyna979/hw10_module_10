from django.forms import ModelForm, CharField, TextInput
from .models import Author, Quote, Tag

class AuthorForm(ModelForm):
    
    class Meta:
        model = Author
        
        fields = ['fullname', 'born_date', 'born_location', 'description']
        
class QuoteForm(ModelForm):
    
    class Meta:
        model = Quote
        
        fields = ['tags', 'author', 'quote']
    
class TagForm(ModelForm):
    
    class Meta:
        model = Tag
        
        fields = ['name']
