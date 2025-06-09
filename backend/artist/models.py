from django.db import models

# Create your models here.
class ArtistRequest(models.Model):
    artist_name = models.CharField(max_length=100)
class ArtistProfile(models.Model):
    artist_name = models.CharField(max_length=100)
    