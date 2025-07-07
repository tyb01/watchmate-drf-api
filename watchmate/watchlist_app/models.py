from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
from django.contrib.auth.models import User
class Platform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200)
    url = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
class Watchlist(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    
    total_reviews = models.IntegerField(default=0)
    avg_reviews = models.FloatField(default=0)
    
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    platform = models.ForeignKey(Platform,on_delete=models.CASCADE,null=True, related_name='watchlist')

    def __str__(self):
        return self.title
    
class Review(models.Model):
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=250)
    watchlist = models.ForeignKey(Watchlist,on_delete=models.CASCADE,related_name="review")