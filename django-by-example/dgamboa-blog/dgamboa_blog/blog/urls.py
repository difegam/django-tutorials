from django.urls import path

from . import views

app_name = "blog"  # Application namespace to avoid conflicts with other apps

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:id>/", views.post_detail, name="post_detail"),
]
# Any value specified in the url pattern is capture as a string
# You can use path converters to capture other data types
# For example, <int:id> will capture an integer value
#              <slug:title> will capture a slug value
# See: https://docs.djangoproject.com/en/5.0/topics/http/urls/#path-converters
