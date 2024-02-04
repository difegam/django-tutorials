from django.urls import path

from . import views

app_name = "blog"  # Application namespace to avoid conflicts with other apps

urlpatterns = [
    # Post views
    # path("", views.post_list, name="post_list"),             # Function based view
    path("", views.PostListView.as_view(), name="post_list"),  # Class based view
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",  # SEO friendly URL
        views.post_detail,
        name="post_detail",
    ),
    # Email post to a friend
    path(
        "<int:post_id>/share/",
        views.post_share,
        name="post_share",
    ),
    # Comment on a post
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
]
# Any value specified in the url pattern is capture as a string
# You can use path converters to capture other data types
# For example, <int:id> will capture an integer value
#              <slug:title> will capture a slug value
# See: https://docs.djangoproject.com/en/5.0/topics/http/urls/#path-converters
