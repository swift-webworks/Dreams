from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Destination, BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["core:home", "core:fleet_list", "core:destination_list", "core:story", "core:blog_list", "core:contact"]

    def location(self, item):
        return reverse(item)


class DestinationSitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return Destination.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()