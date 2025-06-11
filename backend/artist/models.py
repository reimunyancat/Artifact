from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Artist(models.Model):
    artist_name = models.CharField(max_length=200, unique=True)
    introduction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artists')
    is_verified = models.BooleanField(default=False)
    ai_verification_score = models.FloatField(null=True, blank=True)
    ai_verification_notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.artist_name

class ArtistFeature(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=300)
    
    def __str__(self):
        return f"{self.artist.artist_name} - {self.feature_text}"

class Music(models.Model):
    GENRE_CHOICES = [
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
        ('classical', 'Classical'),
        ('hip-hop', 'Hip-Hop'),
        ('electronic', 'Electronic'),
        ('country', 'Country'),
        ('r&b', 'R&B'),
        ('indie', 'Indie'),
        ('other', 'Other'),
    ]
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='musics')
    name = models.CharField(max_length=200)
    publish_date = models.DateField()
    music_link = models.URLField(blank=True, null=True)
    album_name = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.artist.artist_name} - {self.name}"

class Post(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('needs_revision', 'Needs Revision'),
    ]
    
    title = models.CharField(max_length=300)
    content = models.TextField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ai_review_score = models.FloatField(null=True, blank=True)
    ai_review_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
