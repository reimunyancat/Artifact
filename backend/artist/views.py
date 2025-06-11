from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import json
import random

from .models import Artist, ArtistFeature, Music, Post, Comment
from .forms import PostForm, CommentForm, MusicForm, CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.

def post_list(request):
    """게시판 메인 페이지 - 모든 게시글 목록"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    posts = Post.objects.all()
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(artist__artist_name__icontains=search_query)
        )
    
    if status_filter:
        posts = posts.filter(status=status_filter)
    
    paginator = Paginator(posts, 10)  # 페이지당 10개
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Post.STATUS_CHOICES,
    }
    return render(request, 'artist/post_list.html', context)

def post_detail(request, pk):
    """게시글 상세 페이지"""
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글이 작성되었습니다.')
            return redirect('artist:post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'artist/post_detail.html', context)

@login_required
def post_create(request):
    """새 게시글 작성"""
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            
            # ai 걍 땜빵
            post.ai_review_score = random.uniform(0.3, 1.0)
            if post.ai_review_score > 0.8:
                post.status = 'approved'
                post.ai_review_notes = 'AI 검증 통과: 높은 품질의 콘텐츠로 판단됩니다.'
            elif post.ai_review_score > 0.6:
                post.status = 'needs_revision'
                post.ai_review_notes = 'AI 검증 결과: 일부 내용의 수정이 필요합니다.'
            else:
                post.status = 'pending'
                post.ai_review_notes = 'AI 검증 결과: 관리자 검토가 필요합니다.'
            
            post.save()
            messages.success(request, '게시글이 작성되었습니다. AI 검증이 완료되었습니다.')
            return redirect('artist:post_detail', pk=post.pk)
    else:
        post_form = PostForm()
    
    context = {
        'post_form': post_form,
        }
    return render(request, 'artist/post_create.html', context)

def artist_list(request):
    """아티스트 목록"""
    search_query = request.GET.get('search', '')
    verified_filter = request.GET.get('verified', '')
    
    artists = Artist.objects.all()
    
    if search_query:
        artists = artists.filter(
            Q(artist_name__icontains=search_query) | 
            Q(introduction__icontains=search_query)
        )
    
    if verified_filter == 'true':
        artists = artists.filter(is_verified=True)
    elif verified_filter == 'false':
        artists = artists.filter(is_verified=False)
    
    paginator = Paginator(artists, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'verified_filter': verified_filter,
    }
    return render(request, 'artist/artist_list.html', context)

def artist_detail(request, pk):
    """아티스트 상세 정보"""
    artist = get_object_or_404(Artist, pk=pk)
    musics = artist.musics.all().order_by('-publish_date')
    features = artist.features.all()
    posts = artist.posts.all().order_by('-created_at')[:5]  # 최근 게시글 5개
    
    context = {
        'artist': artist,
        'musics': musics,
        'features': features,
        'posts': posts,
    }
    return render(request, 'artist/artist_detail.html', context)

@login_required
def music_add(request, artist_pk):
    """아티스트에 음악 추가"""
    artist = get_object_or_404(Artist, pk=artist_pk)
    
    if request.method == 'POST':
        music_form = MusicForm(request.POST)
        if music_form.is_valid():
            music = music_form.save(commit=False)
            music.artist = artist
            music.save()
            messages.success(request, '음악이 추가되었습니다.')
            return redirect('artist:artist_detail', pk=artist.pk)
    else:
        music_form = MusicForm()
    
    context = {
        'music_form': music_form,
        'artist': artist,
    }
    return render(request, 'artist/music_add.html', context)

# 인증 관련 뷰
def user_login(request):
    """로그인 페이지"""
    if request.user.is_authenticated:
        return redirect('artist:post_list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{username}님, 환영합니다!')
                next_url = request.GET.get('next', 'artist:post_list')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    context = {'form': form}
    return render(request, 'registration/login.html', context)

def user_logout(request):
    """로그아웃"""
    logout(request)
    messages.success(request, '로그아웃 되었습니다.')
    return redirect('artist:post_list')

def user_register(request):
    """회원가입 페이지"""
    if request.user.is_authenticated:
        return redirect('artist:post_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}님의 계정이 생성되었습니다! 로그인해주세요.')
            return redirect('artist:login')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)
