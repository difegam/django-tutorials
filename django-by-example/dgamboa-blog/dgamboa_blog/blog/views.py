from django.http import Http404, HttpResponse
from django.shortcuts import render

from .models import Post


def post_list(request) -> HttpResponse:
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, id: int) -> HttpResponse:
    """Retrieve a published post by id"""
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist as error:
        raise Http404("Post does not exist") from error
    return render(request, "blog/post/detail.html", {"post": post})
