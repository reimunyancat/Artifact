from django.contrib import admin
from .models import Artist, ArtistFeature, Music, Post, Comment

# Register your models here.

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['artist_name', 'created_by', 'is_verified', 'ai_verification_score', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['artist_name', 'introduction']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ArtistFeature)
class ArtistFeatureAdmin(admin.ModelAdmin):
    list_display = ['artist', 'feature_text']
    list_filter = ['artist']

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'publish_date', 'genre', 'album_name']
    list_filter = ['genre', 'publish_date', 'artist']
    search_fields = ['name', 'album_name', 'artist__artist_name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'artist', 'status', 'ai_review_score', 'created_at']
    list_filter = ['status', 'created_at', 'ai_review_score']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
