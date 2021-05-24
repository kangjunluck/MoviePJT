from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

class Movie(models.Model):
    # movieid = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)   
    original_title = models.CharField(max_length=200)
    original_language = models.CharField(max_length=10)
    overview = models.TextField()
    adult = models.BooleanField()
    budget = models.CharField(max_length=20)
    poster_path = models.CharField(max_length=500)
    release_date = models.DateField()
    runtime = models.CharField(max_length=5)
    vote_average = models.CharField(max_length=5)
    video = models.CharField(max_length=500)
    backdrop_path = models.CharField(max_length=500)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
    movie_vote = models.FloatField(default=0)
    def set_genres(self):
        return json.loads(self.genres)

class Review(models.Model):
    person_vote = models.IntegerField()
    content = models.TextField()    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')

