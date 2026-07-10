from django.contrib import admin
from django.utils.html import format_html
from .models import Vehicle, Destination, Story, Memory, ClientReview, ContactSubmission


class ThumbnailMixin:
    def thumbnail(self, obj):
        image = getattr(obj, "image", None) or getattr(obj, "reviewer_image", None)
        if image:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;" />', image.url)
        return "—"
    thumbnail.short_description = "Preview"


@admin.register(Vehicle)
class VehicleAdmin(ThumbnailMixin, admin.ModelAdmin):
    list_display = ("thumbnail", "name", "category", "tier", "price_per_km", "seats", "is_featured", "display_order")
    list_editable = ("is_featured", "display_order")
    list_display_links = ("name",)
    list_filter = ("tier", "category", "is_featured")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Basic Info", {"fields": ("name", "slug", "category", "tier")}),
        ("Pricing & Capacity", {"fields": ("price_per_km", "seats")}),
        ("Media & Description", {"fields": ("image", "description")}),
        ("Display", {"fields": ("is_featured", "display_order")}),
    )


@admin.register(Destination)
class DestinationAdmin(ThumbnailMixin, admin.ModelAdmin):
    list_display = ("thumbnail", "name", "travel_type", "best_season", "is_featured", "display_order")
    list_editable = ("is_featured", "display_order")
    list_display_links = ("name",)
    list_filter = ("travel_type", "best_season", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Basic Info", {"fields": ("name", "slug", "image", "description")}),
        ("Travel Details", {"fields": ("best_time", "best_season", "travel_type")}),
        ("SEO", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
        ("Display", {"fields": ("is_featured", "display_order")}),
    )


@admin.register(Story)
class StoryAdmin(ThumbnailMixin, admin.ModelAdmin):
    list_display = ("thumbnail", "title", "section", "display_order")
    list_editable = ("display_order",)
    list_display_links = ("title",)
    list_filter = ("section",)
    search_fields = ("title", "content")


@admin.register(Memory)
class MemoryAdmin(ThumbnailMixin, admin.ModelAdmin):
    list_display = ("thumbnail", "caption", "display_order")
    list_editable = ("display_order",)
    list_display_links = ("caption",)


@admin.register(ClientReview)
class ClientReviewAdmin(ThumbnailMixin, admin.ModelAdmin):
    list_display = ("thumbnail", "reviewer_name", "rating", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_display_links = ("reviewer_name",)
    list_filter = ("rating", "is_published")
    search_fields = ("reviewer_name", "review_text")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "destination", "travel_days", "members", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "phone", "destination")
    readonly_fields = ("name", "phone", "destination", "pickup_location", "travel_days", "members", "ip_address", "created_at")

    def has_add_permission(self, request):
        return False


admin.site.site_header = "Dreams Tours and Travels — Admin"
admin.site.site_title = "Dreams Admin"
admin.site.index_title = "Manage Website Content"
