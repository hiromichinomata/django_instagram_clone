from multiprocessing import context
from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from comment.forms import NewCommentForm
from comment.models import Comment
from post.forms import NewPostForm
from post.models import Likes, Tag, Stream, Follow, Post
from django.contrib.auth.decorators import login_required

from userauths.models import Profile

# Create your views here.

def index(request):
  user = request.user
  posts = Stream.objects.filter(user=user)

  group_ids = []
  for post in posts:
    group_ids.append(post.post_id)

  post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
  context = {
    'post_items': post_items
  }

  return render(request, 'index.html', context)

def NewPost(request):
  user = request.user
  tags_objs = []

  if request.method == "POST":
    form = NewPostForm(request.POST, request.FILES)
    if form.is_valid():
      picture = form.cleaned_data.get('picture')
      caption = form.cleaned_data.get('caption')
      tag_form = form.cleaned_data.get('tag')
      tags_list = list(tag_form.split(','))

      for tag in tags_list:
        t, created = Tag.objects.get_or_create(title=tag)
        tags_objs.append(t)
      p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id =user.id)
      p.tag.set(tags_objs)
      p.save()
      return redirect('index')
  else:
    form = NewPostForm()
  context = {
    'form': form
  }
  return render(request, 'newpost.html', context)

def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }

    return render(request, 'post-detail.html', context)

def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))

def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))
