"""
Template tags for the blog app
https://docs.djangoproject.com/en/4.2/ref/templates/builtins/
"""

from django import template

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts() -> int:
    """Template tag that return the total number of published posts."""
    return Post.published.count()
