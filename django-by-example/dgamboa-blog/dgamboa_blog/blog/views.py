from dgamboa_blog.dgamboa.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post


# Post List view
class PostListView(ListView):
    """List all published posts using class based view"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request, tag_slug=None) -> HttpResponse:
    """List all published posts using function based view"""

    posts = Post.published.all()

    # filter by tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # paginator -> 3 posts per page
    paginator = Paginator(posts, 3)  # Create a paginator object
    page_number = request.GET.get("page", 1)  # Get page number, default 1
    try:
        posts_on_page = paginator.page(page_number)  # return given page number
    except EmptyPage:  # If page is out of range
        posts_on_page = paginator.page(paginator.num_pages)  # return last page
    except PageNotAnInteger:  # If page is not an integer
        posts_on_page = paginator.page(1)  # return first page

    return render(request, "blog/post/list.html", {"posts": posts_on_page, "tag": tag})


# Post Detail view
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
    # Add comments
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = (
        Post.published.filter(tags__in=post_tags_ids)  # Get posts with same tags
        .exclude(id=post.id)  # Exclude current post
        .annotate(same_tags=Count("tags"))  # Count the number of tags in common
        .order_by("-same_tags", "-publish")[:4]  # Order by tags & publish date
    )

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


# Form view
def post_share(request, post_id: int) -> HttpResponse:
    """Share a post by email"""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":  # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():  # Form fields passed validation
            cleaned_data = form.cleaned_data
            print(cleaned_data, EMAIL_HOST_USER)
            subject = f"{cleaned_data['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post.get_absolute_url()}\n\n"
                f"{cleaned_data['name']}'s comments: {cleaned_data['comments']}"
            )
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [cleaned_data["to"]],
                fail_silently=False,
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


@require_POST
def post_comment(request, post_id: int) -> HttpResponse:
    """Create a comment for a post"""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
