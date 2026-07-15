from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r"^[6-9]\d{9}$",
    message="Enter a valid 10-digit Indian mobile number."
)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vehicle(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("sedan", "Sedan"),
        ("suv", "SUV"),
        ("maxi", "Maxi / Tempo Traveller"),
    ]
    TIER_CHOICES = [
        ("budget", "Budget Friendly"),
        ("premium", "Premium"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="sedan")
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="budget")
    price_per_km = models.DecimalField(max_digits=6, decimal_places=2, help_text="Price per KM in ₹")
    seats = models.CharField(max_length=20, help_text="e.g. 4+1, 6+1, 18+1")
    image = models.ImageField(upload_to="fleet/", help_text="Recommended: 1200x800 WebP/JPG")
    description = models.CharField(max_length=220, help_text="Short one-line description")
    is_featured = models.BooleanField(default=False, help_text="Show on Home page (max 3 recommended)")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "price_per_km"]
        verbose_name = "Vehicle"
        verbose_name_plural = "Fleet — Vehicles"

    def __str__(self):
        return f"{self.name} ({self.get_tier_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:fleet_list") + f"#{self.slug}"


class Destination(TimeStampedModel):
    TRAVEL_TYPE_CHOICES = [
        ("family", "Family"),
        ("couples", "Couples"),
        ("pilgrimage", "Pilgrimage"),
        ("friends", "Friends"),
        ("adventure", "Adventure"),
    ]
    SEASON_CHOICES = [
        ("summer", "Summer"),
        ("winter", "Winter"),
        ("monsoon", "Monsoon"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to="destinations/", help_text="Recommended: 1200x900 WebP/JPG")
    description = models.TextField(help_text="Short description used on cards and detail page")
    best_time = models.CharField(max_length=100, help_text="e.g. October to April")
    best_season = models.CharField(max_length=10, choices=SEASON_CHOICES, default="winter")
    travel_type = models.CharField(max_length=15, choices=TRAVEL_TYPE_CHOICES, default="family")
    is_featured = models.BooleanField(default=False, help_text="Show on Home page (max 3 recommended)")
    meta_title = models.CharField(max_length=70, blank=True, help_text="Leave blank to auto-generate")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Leave blank to auto-generate")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:destination_detail", kwargs={"slug": self.slug})

    def get_meta_title(self):
        return self.meta_title or f"{self.name} Tour Packages | Dreams Tours and Travels"

    def get_meta_description(self):
        return self.meta_description or self.description[:157].rsplit(" ", 1)[0] + "..."


class Story(TimeStampedModel):
    SECTION_CHOICES = [
        ("owner", "Owner Introduction"),
        ("staff", "Staff Timeline Profile"),
    ]

    section = models.CharField(max_length=10, choices=SECTION_CHOICES, default="staff")
    title = models.CharField(max_length=150, help_text="Name / role, e.g. 'Selvam — Founder & Head Driver'")
    content = models.TextField(help_text="Rich text supported (basic HTML)")
    image = models.ImageField(upload_to="story/")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["section", "display_order"]
        verbose_name = "Story Profile"
        verbose_name_plural = "Our Story — Profiles"

    def __str__(self):
        return self.title


class Memory(TimeStampedModel):
    image = models.ImageField(upload_to="memories/", help_text="Recommended: square 800x800")
    caption = models.CharField(max_length=150, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Memory Photo"
        verbose_name_plural = "Memories Gallery"

    def __str__(self):
        return self.caption or f"Memory #{self.pk}"


class ClientReview(TimeStampedModel):
    reviewer_name = models.CharField(max_length=100)
    reviewer_image = models.ImageField(upload_to="reviews/", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    review_text = models.TextField(max_length=500)
    google_review_url = models.URLField(blank=True, help_text="Link to the review on Google")
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Client Review"
        verbose_name_plural = "Client Stories — Reviews"

    def __str__(self):
        return f"{self.reviewer_name} ({self.rating}★)"


class ContactSubmission(TimeStampedModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, validators=[phone_validator])
    destination = models.CharField(max_length=150)
    pickup_location = models.CharField(max_length=150)
    travel_days = models.PositiveSmallIntegerField(default=1)
    members = models.PositiveSmallIntegerField(default=1)
    ROOM_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    room_booking = models.CharField(
        max_length=3,
        choices=ROOM_CHOICES,
        default="No"
    )

    location_place = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    is_read = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact / Enquiry"
        verbose_name_plural = "Contact Enquiries"

    def __str__(self):
        return f"{self.name} — {self.destination}"


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog — Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    featured_image = models.ImageField(upload_to="blog/", help_text="Recommended: 1200x800 WebP/JPG")
    excerpt = models.CharField(max_length=220, help_text="Short summary shown on blog cards")
    content = models.TextField(
        help_text="Full article content. Basic HTML allowed: <p>, <h2>, <strong>, <em>, <ul>/<li>, <a>, <img>"
    )
    author = models.CharField(max_length=100, default="Dreams Tours and Travels")
    published_date = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=False, help_text="Uncheck to keep this post as a draft")
    is_featured = models.BooleanField(default=False, help_text="Show on Home page (max 3 recommended)")
    meta_title = models.CharField(max_length=70, blank=True, help_text="Leave blank to auto-generate")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Leave blank to auto-generate")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-published_date", "display_order"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog — Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:blog_detail", kwargs={"slug": self.slug})

    def get_meta_title(self):
        return self.meta_title or f"{self.title} | Dreams Tours and Travels Blog"

    def get_meta_description(self):
        return self.meta_description or self.excerpt
    
class Service(TimeStampedModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50, default="bi-compass",
        help_text="Bootstrap Icons class name, e.g. bi-compass, bi-house-door, bi-car-front, bi-geo-alt"
    )
    description = models.CharField(max_length=220, help_text="Short one-line description shown on the card")
    badge_text = models.CharField(max_length=60, default="Budget & Premium")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Service"
        verbose_name_plural = "Fleet Page — Services"

    def __str__(self):
        return self.name