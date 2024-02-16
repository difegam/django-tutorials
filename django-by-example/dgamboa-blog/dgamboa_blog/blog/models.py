from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# Custom model manager for published posts
class PostPublishedManager(models.Manager):
    """Custom model manager for published posts"""

    def get_queryset(self):
        return super().get_queryset().filter(status="PB")


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )  # Many-to-one relationship
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    # Tags
    tags = TaggableManager()

    # Model managers
    # If you define a custom manager, you have to explicitly define the default manager
    objects = models.Manager()  # default manager

    # Custom manager allow to retrieve all published posts
    # Post.published.all() instead of Post.objects.all().filter(status="PB")
    published = PostPublishedManager()  # custom manager

    class Meta:
        ordering = ("-publish",)  # `-` means from newest to oldest
        indexes = (
            models.Index(
                fields=["publish"],
            ),  # indexes improve performance when filtering or sorting
        )

    def __str__(self) -> str:
        """Return a string representation of a post"""
        return self.title

    def get_absolute_url(self) -> str:
        """Return the canonical URL for a post"""
        return reverse(
            "blog:post_detail",
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "slug": self.slug,
            },
        )


# Comments model
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)
        indexes = (
            models.Index(
                fields=["created"],
            ),
        )

    def __str__(self) -> str:
        """Return a string representation of a comment"""
        return f"Comment by {self.name} on {self.post}"

    # def get_absolute_url(self) -> str:
    #     """Return the canonical URL for a post"""
    #     return reverse(
    #         "blog:post_list",
    #     )
