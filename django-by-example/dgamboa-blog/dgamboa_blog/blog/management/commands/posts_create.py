from dataclasses import dataclass
from random import choice, randint
from typing import TypedDict

import requests
from blog.models import Post
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from typing_extensions import NotRequired

# Post data from DummyJSON
POSTS_URL = "https://dummyjson.com/posts"


@dataclass
class DummyData:
    total: int
    skip: int
    limit: int
    posts: list[dict]

    def __str__(self) -> str:
        return f"Total Posts: {self.limit}, Skip: {self.skip}"

    def list_posts(self) -> list[dict]:
        return self.posts


class Params(TypedDict):
    limit: NotRequired[str | int]
    skip: NotRequired[str | int]


def get_api_data(url: str, params: Params | None = None) -> dict:
    """Get dummy data from an API"""
    response = requests.get(url, params=params, timeout=5)
    if not response.ok:
        raise CommandError(f"Failed to fetch data from {url}")
    return response.json()


def create_posts(data: list[dict], user_id: int = 1) -> None:
    """Create posts from dummy data"""
    user = User.objects.get(id=user_id)
    for post_data in data:
        post = Post(
            title=post_data["title"],
            slug=slugify(post_data["title"]),
            body=post_data["body"],
            author=user,
            status=choice([Post.Status.PUBLISHED, Post.Status.DRAFT]),
        )
        post.save()
        post.tags.add(*post_data["tags"])


class Command(BaseCommand):
    help = "Mock Book data"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "limit",
            type=int,
            nargs="?",
            default=10,
            help="Number of posts to fetch and create",
        )
        parser.add_argument(
            "-s",
            "--skip",
            type=int,
            nargs="?",
            default=0,
            help="Number of posts to skip",
        )

    def handle(self, *args, **options) -> None:
        limit = options["limit"]
        skip = options["skip"] or randint(1, 50)

        params = {"limit": limit, "skip": skip}
        posts = get_api_data(POSTS_URL, params)
        dummy_data = DummyData(**posts)
        create_posts(dummy_data.list_posts())

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully fetched and created {dummy_data.limit} posts"
            )
        )
