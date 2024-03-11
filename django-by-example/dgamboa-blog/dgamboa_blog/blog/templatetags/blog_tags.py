"""
Template tags for the blog app
https://docs.djangoproject.com/en/4.2/ref/templates/builtins/
"""

from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/#simple-tags
#
@register.simple_tag
def total_posts() -> int:
    """Template tag that return the total number of published posts."""
    return Post.published.count()


# https://docs.djangoproject.com/en/dev/topics/db/aggregation/#cheat-sheet
#
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/#inclusion-tags
#
@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count: int = 5) -> dict:
    """Template tag that return the latest published posts."""
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}
