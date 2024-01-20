from math import e

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request) -> HttpResponse:
    posts = Post.published.all()
    # paginator -> 3 posts per page
    paginator = Paginator(posts, 3)  # Create a paginator object
    page_number = request.GET.get("page", 1)  # Get page number, default 1
    try:
        posts_on_page = paginator.page(page_number)  # return given page number
    except EmptyPage:  # If page is out of range
        posts_on_page = paginator.page(paginator.num_pages)  # return last page
    except PageNotAnInteger:  # If page is not an integer
        posts_on_page = paginator.page(1)  # return first page

    return render(request, "blog/post/list.html", {"posts": posts_on_page})


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
