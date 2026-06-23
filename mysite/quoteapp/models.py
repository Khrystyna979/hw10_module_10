from django.db import models
from django.contrib.auth.models import User

# Create your models here.    
class Author(models.Model):
    fullname = models.CharField(max_length=150, unique=True)
    born_date = models.CharField(max_length=150)
    born_location = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f'{self.fullname}'
    
class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)    
    
    def __str__(self):
        return f'{self.name}'
    
class Quote(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f'{self.quote}'
    