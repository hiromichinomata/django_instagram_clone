from multiprocessing import context
from turtle import title
from django.shortcuts import redirect, render
from post.forms import NewPostForm
from post.models import Tag, Stream, Follow, Post
from django.contrib.auth.decorators import login_required

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
