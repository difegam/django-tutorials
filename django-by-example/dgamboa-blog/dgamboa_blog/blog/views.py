from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request) -> HttpResponse:
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year: int, month: int, day: int, slug: str) -> HttpResponse:
    """Retrieve a published post by id"""
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})
