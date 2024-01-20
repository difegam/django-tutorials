# Utils

## Create dummy data

This is a view that creates dummy data for testing purposes. It uses the [JSONPlaceholder](https://jsonplaceholder.typicode.com/) API to get the data.

`blog/url.py`

```python
urlpatterns = [
    # ...,
    path("create-dummy-data/", create_dummy_data, name="create_dummy_data"),
]

```

`blog/views.py`

```python

def create_dummy_data(request):
    """Create dummy data for testing"""
    import random

    from django.contrib.auth.models import User
    from django.http import JsonResponse
    from django.template.defaultfilters import slugify

    data = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=5)

    user, created = User.objects.get_or_create(
        username="test_user", email="mail@gmail.com"
    )
    if created:
        user.set_password("123")
        user.save()

    for post in data.json():
        Post.objects.create(
            title=post["title"],
            slug=slugify(post["title"]),
            body=post["body"],
            author=user,
            status=random.choice(["DF", "PB"]),
        )
        print(f"Created post: {post['title']}")
    return JsonResponse({"data": data.json(), "status": "success"})
```
