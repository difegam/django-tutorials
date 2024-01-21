from dgamboa_blog.dgamboa.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


# Post List view
class PostListView(ListView):
    """List all published posts using class based view"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request) -> HttpResponse:
    """List all published posts using function based view"""

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
    return render(request, "blog/post/detail.html", {"post": post})


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
