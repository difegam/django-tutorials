from django.contrib import admin

from .models import Comment, Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "publish",
        "status",
    )  # Display fields in admin
    list_filter = ("status", "created", "publish", "author")  # Filter in sidebar
    search_fields = ("title", "body")  # Search by title and body
    prepopulated_fields = {
        "slug": ("title",)
    }  # Slug field will be filled automatically
    raw_id_fields = ("author",)  # Lookup author instead of dropdown
    date_hierarchy = "publish"  # Generate navigation by date
    ordering = ("status", "publish")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "post", "created", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "email", "body")
