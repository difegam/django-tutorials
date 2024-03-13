from django.contrib.sitemaps import Sitemap

from .models import Post


# https://docs.djangoproject.com/en/5.0/ref/contrib/sitemaps/
class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
