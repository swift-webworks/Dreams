from django.conf import settings


def company_info(request):
    """Makes company details available in every template without repeating queries."""
    return {
        "COMPANY_NAME": "Dreams Tours and Travels",
        "COMPANY_PHONE": "7708155016",
        "COMPANY_PHONE_DISPLAY": "+91 77081 55016",
        "COMPANY_WHATSAPP_LINK": "https://wa.me/917708155016",
        "COMPANY_EMAIL": "toursandtravelsdreams@gmail.com",
        "COMPANY_ADDRESS_LINE1": "Easwari Amman Kovil Street",
        "COMPANY_ADDRESS_LINE2": "Nearby Temple Road",
        "COMPANY_CITY": "Rameswaram, Tamil Nadu - 623518",
        "SITE_URL": getattr(settings, "SITE_URL", "https://www.dreamstourstravel.in"),
        "GOOGLE_MAP_EMBED": (
            "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3917.0!2d79.3129!3d9.2876"
            "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sRameswaram%2C+Tamil+Nadu!5e0!3m2!1sen!2sin"
        ),
    }
