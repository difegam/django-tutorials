from blog.models import Post
from django.db import connection

items = slice(0, 2)


def run() -> None:
    posts = Post.objects.all()[items]  # Return all the posts as a QuerySet
    print("\nPosts Object: \n", posts)
    posts_values = Post.objects.values("title", "slug")[
        items
    ]  # Return a QuerySet of dictionaries with the title and slug of all the posts
    print("SQL Qry: ", connection.queries)
    print("\nPosts Values: \n", posts_values)
    posts_values_list = Post.objects.values_list("title", "slug")[
        items
    ]  # Return a QuerySet of tuples with the title and slug of all the posts
    print("\nPosts Values List: \n", posts_values_list)


# Run the script
# python manage.py runscript orm_script
# poetry run python manage.py runscript orm_script
