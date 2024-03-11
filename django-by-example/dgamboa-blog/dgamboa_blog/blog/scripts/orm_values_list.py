from blog.models import Post
from django.db import connection

items = slice(0, 2)


def run() -> None:

    posts_values = Post.objects.values_list("title", "slug")[
        items
    ]  # Return a QuerySet list of tuples with the title and slug of all the posts
    print("\nPosts Values: \n", posts_values)
    posts_values_flat = Post.objects.values_list("title", flat=True)
    print(
        "\nPosts Values List: \n", posts_values_flat
    )  # Return a QuerySet list of the title of all the posts


# Run the script
# python manage.py runscript orm_values_list
# poetry run python manage.py runscript orm_values_list
