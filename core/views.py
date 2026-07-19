from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponse

from .models import Vehicle, Destination, Story, Memory, ClientReview, BlogCategory, BlogPost, Service, RoomBooking
from .forms import ContactForm, RoomBookingForm


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def home(request):
    context = {
        "meta_title": "Dreams Tours and Travels — Rameswaram Taxi & Tour Packages",
        "meta_description": "Book comfortable, safe and affordable taxi & tour packages from Rameswaram. "
                             "Sedans, SUVs & Tempo Travellers for pilgrimage, family and group trips across South India.",
        "canonical_path": "",
        "featured_vehicles": Vehicle.objects.filter(is_featured=True)[:3],
        "featured_destinations": Destination.objects.filter(is_featured=True)[:3],
        "memories": Memory.objects.all()[:16],
        "reviews": ClientReview.objects.filter(is_published=True)[:6],
        "featured_posts": BlogPost.objects.filter(is_published=True, is_featured=True)[:3],
        "contact_form": ContactForm(),
    }
    return render(request, "core/home.html", context)


def fleet_list(request):
    tier = request.GET.get("tier", "budget")
    if tier not in ("budget", "premium"):
        tier = "budget"
    vehicles = Vehicle.objects.filter(tier=tier)
    context = {
        "services": Service.objects.filter(is_active=True),
        "meta_title": "Our Fleet — Sedans, SUVs & Tempo Travellers | Dreams Tours and Travels",
        "meta_description": "Explore our complete fleet of budget and premium vehicles — sedans, SUVs, "
                             "and tempo travellers — available for hire in Rameswaram and across Tamil Nadu.",
        "canonical_path": "/fleet/",
        "vehicles": vehicles,
        "active_tier": tier,
    }
    return render(request, "core/fleet_list.html", context)


def destination_list(request):
    destinations = Destination.objects.all()

    query = request.GET.get("q", "").strip()
    travel_type = request.GET.get("travel_type", "")
    season = request.GET.get("season", "")

    if query:
        destinations = destinations.filter(name__icontains=query)
    if travel_type:
        destinations = destinations.filter(travel_type=travel_type)
    if season:
        destinations = destinations.filter(best_season=season)

    context = {
        "meta_title": "Popular Tourist Destinations Near Rameswaram | Dreams Tours and Travels",
        "meta_description": "Discover Rameswaram, Madurai, Dhanushkodi, Kanyakumari and more. "
                             "Filter destinations by travel type and best season, then book your trip today.",
        "canonical_path": "/destinations/",
        "destinations": destinations,
        "query": query,
        "travel_type": travel_type,
        "season": season,
        "travel_type_choices": Destination.TRAVEL_TYPE_CHOICES,
        "season_choices": Destination.SEASON_CHOICES,
    }
    return render(request, "core/destination_list.html", context)


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    related = Destination.objects.exclude(pk=destination.pk)[:3]
    context = {
        "meta_title": destination.get_meta_title(),
        "meta_description": destination.get_meta_description(),
        "canonical_path": f"/destinations/{destination.slug}/",
        "destination": destination,
        "related_destinations": related,
    }
    return render(request, "core/destination_detail.html", context)


def story(request):
    owner = Story.objects.filter(section="owner").first()
    staff = Story.objects.filter(section="staff")
    context = {
        "meta_title": "Our Story — Why Choose Dreams Tours and Travels",
        "meta_description": "10+ years of trusted, safe travel across South India. Meet our founder and "
                             "professional driving team behind Dreams Tours and Travels, Rameswaram.",
        "canonical_path": "/our-story/",
        "owner": owner,
        "staff": staff,
    }
    return render(request, "core/story.html", context)


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        ip = get_client_ip(request)
        cache_key = f"contact_rate_{ip}"
        submissions = cache.get(cache_key, 0)
        if submissions >= 5:
            messages.error(request, "Too many submissions. Please try again later or contact us via WhatsApp.", extra_tags="trip")
            return redirect("core:contact")

        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.ip_address = ip
            submission.save()
            cache.set(cache_key, submissions + 1, timeout=3600)
            messages.success(request, "Thank you! We'll contact you shortly on WhatsApp/Call.", extra_tags="trip")
            return redirect("core:contact")
        else:
            messages.error(request, "Please correct the errors below.", extra_tags="trip")
    else:
        form = ContactForm()

    context = {
        "meta_title": "Contact Us — Plan Your Trip | Dreams Tours and Travels",
        "meta_description": "Get in touch with Dreams Tours and Travels, Rameswaram. Call, WhatsApp or "
                             "fill our enquiry form to plan your next journey.",
        "canonical_path": "/contact/",
        "contact_form": form,
        "room_booking_form": RoomBookingForm(),
    }
    return render(request, "core/contact.html", context)


@require_http_methods(["GET", "POST"])
def room_booking(request):
    if request.method == "POST":
        ip = get_client_ip(request)
        cache_key = f"room_booking_rate_{ip}"
        submissions = cache.get(cache_key, 0)
        if submissions >= 5:
            messages.error(request, "Too many submissions. Try WhatsApp instead.", extra_tags="room")
            return redirect("core:contact")
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.ip_address = ip
            booking.save()
            cache.set(cache_key, submissions + 1, timeout=3600)
            messages.success(request, "Thank you! We'll confirm your room booking shortly.", extra_tags="room")
            return redirect("core:contact")
        else:
            messages.error(request, "Please correct the errors in the room booking form.", extra_tags="room")
    else:
        form = RoomBookingForm()
    context = {
        "meta_title": "Contact Us — Plan Your Trip | Dreams Tours and Travels",
        "canonical_path": "/contact/",
        "contact_form": ContactForm(),
        "room_booking_form": form,
    }
    return render(request, "core/contact.html", context)


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    category_slug = request.GET.get("category", "")
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    context = {
        "meta_title": "Travel Blog — Guides, Tips & Stories | Dreams Tours and Travels",
        "meta_description": "Travel guides, tips and stories from Dreams Tours and Travels — plan your "
                             "next trip across South India with local insights from Rameswaram.",
        "canonical_path": "/blog/",
        "posts": posts,
        "categories": BlogCategory.objects.all(),
        "active_category": category_slug,
    }
    return render(request, "core/blog_list.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)
    if post.category:
        related_posts = related_posts.filter(category=post.category)
    related_posts = related_posts[:3]

    context = {
        "meta_title": post.get_meta_title(),
        "meta_description": post.get_meta_description(),
        "canonical_path": f"/blog/{post.slug}/",
        "post": post,
        "related_posts": related_posts,
    }
    return render(request, "core/blog_detail.html", context)

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
