from django.db import models
from django.utils import timezone


# Create your models here.
class Post:
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ("-publish",)  # - means from newest to oldest
        indexes = (
            models.Index(
                fields=["publish"],
            ),  # indexes improve performance when filtering or sorting
        )

    def __str__(self):
        return self.title
