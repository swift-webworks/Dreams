from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Vehicle, Destination, Story, ClientReview

# Minimal 1x1 transparent PNG used as a stand-in image until real photos are uploaded.
PLACEHOLDER_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
    b"\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


class Command(BaseCommand):
    help = "Seeds the database with sample Fleet, Destination, Story and Review data."

    def handle(self, *args, **options):
        self.seed_vehicles()
        self.seed_destinations()
        self.seed_story()
        self.seed_reviews()
        self.stdout.write(self.style.SUCCESS("Sample data seeded successfully."))

    def placeholder_image(self, name):
        return ContentFile(PLACEHOLDER_PNG, name=name)

    def seed_vehicles(self):
        vehicles = [
            # Budget - Sedan
            ("Xcent", "sedan", "budget", 12, "4+1", "Compact and fuel-efficient sedan, ideal for city and short pilgrimage trips."),
            ("Dzire", "sedan", "budget", 13, "4+1", "Spacious sedan with ample boot space for luggage-heavy trips."),
            ("Etios", "sedan", "budget", 14, "4+1", "Reliable and comfortable sedan for long-distance highway travel."),
            # Budget - SUV
            ("Lodgy", "suv", "budget", 16, "6+1", "Roomy SUV with flexible seating for small family groups."),
            ("Ertiga", "suv", "budget", 17, "6+1", "Popular MPV offering great comfort for family trips."),
            ("Tavera", "suv", "budget", 18, "7+1", "Sturdy SUV suited for longer group journeys and hill routes."),
            # Budget - Maxi
            ("Tourister Non AC", "maxi", "budget", 28, "18+1", "Large capacity non-AC coach for big groups and pilgrimages."),
            # Premium - Sedan
            ("Ciaz", "sedan", "premium", 14, "4+1", "Premium sedan with plush interiors for a smooth, quiet ride."),
            # Premium - SUV
            ("Marazzo", "suv", "premium", 19, "7+1", "Premium MPV with generous legroom and modern comfort features."),
            ("Innova", "suv", "premium", 20, "7+1", "India's most trusted premium SUV for family and business travel."),
            ("Crysta", "suv", "premium", 22, "7+1", "Top-tier SUV with luxury seating and superior ride quality."),
            # Premium - Maxi
            ("Tempo Traveller 14+1 AC", "maxi", "premium", 35, "14+1", "AC tempo traveller with pushback seats for medium groups."),
            ("Tempo Traveller 18+1 AC", "maxi", "premium", 43, "18+1", "Premium AC tempo traveller for larger group pilgrimages and tours."),
        ]
        for i, (name, category, tier, price, seats, desc) in enumerate(vehicles):
            vehicle, created = Vehicle.objects.get_or_create(
                name=name,
                defaults=dict(
                    category=category, tier=tier, price_per_km=price, seats=seats,
                    description=desc, display_order=i,
                    is_featured=name in ("Dzire", "Innova", "Tempo Traveller 14+1 AC"),
                )
            )
            if created and not vehicle.image:
                vehicle.image.save(f"{vehicle.slug}.png", self.placeholder_image(f"{vehicle.slug}.png"), save=True)

    def seed_destinations(self):
        destinations = [
            # --- Tamil Nadu (original) ---
            ("Rameswaram", "family", "winter", "October to March",
             "Home to the sacred Ramanathaswamy Temple and the iconic Pamban Bridge, Rameswaram is one of the holiest pilgrimage sites in India, with pristine beaches nearby.", True),
            ("Madurai", "pilgrimage", "winter", "October to March",
             "Famous for the ancient Meenakshi Amman Temple, Madurai is a vibrant temple city rich in culture, history and South Indian cuisine.", True),
            ("Dhanushkodi", "adventure", "winter", "November to February",
             "A ghost town at the tip of the Indian peninsula where the Bay of Bengal meets the Indian Ocean — perfect for scenic day trips.", True),
            ("Kanyakumari", "family", "winter", "October to February",
             "The southernmost tip of India, known for stunning sunrise and sunset views over three converging seas.", False),
            ("Thanjavur", "pilgrimage", "winter", "November to February",
             "Home to the UNESCO World Heritage Brihadeeswarar Temple and a rich legacy of Chola-era art and architecture.", False),
            ("Kutralam", "adventure", "monsoon", "June to September",
             "Known as the 'Spa of South India', famous for its therapeutic waterfalls best visited during monsoon.", False),
            ("Kodaikanal", "couples", "summer", "April to June",
             "A serene hill station with misty lakes, pine forests and pleasant weather — ideal for a romantic getaway.", False),
            ("Ooty", "family", "summer", "April to June",
             "The 'Queen of Hill Stations' offering tea gardens, botanical gardens and a toy train experience.", False),
            ("Munnar", "couples", "summer", "September to May",
             "Rolling tea plantations and cool climate make Munnar a favourite for couples and nature lovers.", False),
            ("Yercaud", "friends", "summer", "April to June",
             "A quiet hill station perfect for group getaways with coffee estates and scenic viewpoints.", False),
            ("Coonoor", "couples", "summer", "April to June",
             "A quieter alternative to Ooty with sweeping viewpoints, tea estates and colonial-era charm — great for couples.", False),
            ("Yelagiri", "friends", "summer", "March to June",
             "A lesser-known hill station with a scenic lake, trekking trails and adventure sports, ideal for group trips.", False),
            ("Valparai", "adventure", "monsoon", "June to September",
             "A misty plateau in the Western Ghats known for hairpin roads, wildlife sightings and tea plantations.", False),
            ("Palani", "pilgrimage", "winter", "October to March",
             "One of the six abodes of Lord Murugan, Palani is a major pilgrimage hill temple reached by rope-car or foot.", False),

            # --- Kerala ---
            ("Alleppey", "couples", "winter", "November to February",
             "Known as the 'Venice of the East', Alleppey's backwaters and houseboat cruises make it a favourite romantic escape.", True),
            ("Kumarakom", "couples", "winter", "November to February",
             "A tranquil backwater village on Vembanad Lake, famous for houseboats, bird sanctuaries and Ayurvedic resorts.", False),
            ("Varkala", "couples", "winter", "November to February",
             "A dramatic cliffside beach town with sea-facing cafes and sunset views, perfect for a relaxed couples trip.", False),
            ("Vagamon", "couples", "monsoon", "June to September",
             "Rolling green meadows, pine forests and mist-covered hills make Vagamon a peaceful monsoon retreat.", False),
            ("Ponmudi", "couples", "monsoon", "June to September",
             "A quiet hill station near Thiruvananthapuram with winding roads, waterfalls and lush monsoon greenery.", False),
            ("Thekkady", "family", "winter", "October to March",
             "Home to Periyar Wildlife Sanctuary, Thekkady offers boat safaris, spice plantations and forest treks for the whole family.", False),
            ("Kovalam", "friends", "winter", "November to February",
             "A popular crescent beach destination near Thiruvananthapuram, known for its lighthouse and lively beachside cafes.", False),
            ("Wayanad", "adventure", "winter", "October to March",
             "A biodiversity-rich hill district with trekking trails, caves, waterfalls and wildlife sanctuaries.", False),
            ("Athirapally", "friends", "monsoon", "June to September",
             "Often called the 'Niagara of India', these thundering waterfalls are at their most spectacular during monsoon.", False),
            ("Idukki", "family", "monsoon", "June to September",
             "Known for its massive arch dam and lush hill terrain, Idukki is a scenic monsoon destination for family trips.", False),

            # --- Karnataka ---
            ("Coorg", "couples", "winter", "October to March",
             "Known as the 'Scotland of India', Coorg's coffee plantations and cool climate make it a top romantic hill getaway.", False),
            ("Chikmagalur", "couples", "monsoon", "June to September",
             "Rolling coffee estates and misty peaks make Chikmagalur a scenic monsoon retreat, especially for couples.", False),
            ("Mysore", "family", "winter", "October to February",
             "Famous for the illuminated Mysore Palace, Dasara festivities and sprawling gardens — a great family heritage trip.", False),
            ("Gokarna", "friends", "winter", "October to February",
             "A laid-back temple town with unspoilt beaches, popular with groups looking for a relaxed coastal getaway.", False),
            ("Hampi", "adventure", "winter", "October to February",
             "A UNESCO World Heritage site with sprawling ancient ruins, boulder-strewn landscapes and rock climbing spots.", False),
            ("Bandipur", "adventure", "winter", "October to March",
             "A renowned tiger reserve offering jeep safaris and wildlife spotting amid the Western Ghats foothills.", False),

            # --- Extra coverage for family & group trips ---
            ("Kotagiri", "family", "summer", "April to June",
             "The oldest and quietest of the Nilgiri hill stations, known for tea gardens, waterfalls and cool weather.", False),
            ("Marari Beach", "family", "monsoon", "June to September",
             "A peaceful Kerala fishing village beach, lush and green through monsoon, ideal for a quiet family break.", False),
            ("Meghamalai", "friends", "monsoon", "June to September",
             "Known as the 'High Wavy Mountains', this offbeat Western Ghats retreat is a favourite for group trekking trips.", False),
        ]
        for i, (name, ttype, season, best_time, desc, featured) in enumerate(destinations):
            dest, created = Destination.objects.get_or_create(
                name=name,
                defaults=dict(
                    travel_type=ttype, best_season=season, best_time=best_time,
                    description=desc, is_featured=featured, display_order=i,
                )
            )
            if created and not dest.image:
                dest.image.save(f"{dest.slug}.png", self.placeholder_image(f"{dest.slug}.png"), save=True)
    def seed_story(self):
        owner, created = Story.objects.get_or_create(
            section="owner",
            title="R. Selvakumar — Founder & Managing Director",
            defaults=dict(
                content="With over 10 years in the travel industry, Selvakumar built Dreams Tours and Travels "
                        "on a simple promise: every traveller reaches home safely, comfortably, and on time. "
                        "What began as a single sedan has grown into a trusted fleet serving thousands of "
                        "families and pilgrims across South India.",
                display_order=0,
            )
        )
        if created and not owner.image:
            owner.image.save("owner.png", self.placeholder_image("owner.png"), save=True)

        staff = [
            ("Murugan — Senior Driver, 12 Years Experience", "Specialist in pilgrimage routes with an unmatched safety record."),
            ("Rajesh — Operations Manager", "Coordinates bookings and ensures every trip runs on schedule."),
            ("Anitha — Customer Relations", "Your first point of contact for planning the perfect itinerary."),
            ("Karthik — Senior Driver, 8 Years Experience", "Expert in hill-station routes across Tamil Nadu and Kerala."),
            ("Suresh — Fleet Maintenance Head", "Ensures every vehicle is safety-checked before each journey."),
        ]
        for i, (title, content) in enumerate(staff, start=1):
            member, created = Story.objects.get_or_create(
                section="staff", title=title,
                defaults=dict(content=content, display_order=i)
            )
            if created and not member.image:
                member.image.save(f"staff-{i}.png", self.placeholder_image(f"staff-{i}.png"), save=True)

    def seed_reviews(self):
        reviews = [
            ("Priya Ramesh", 5, "Excellent service from Rameswaram to Madurai. The driver was punctual, "
                                 "polite and the car was spotless. Highly recommend for family trips!"),
            ("Arun Kumar", 5, "Booked a Tempo Traveller for our group pilgrimage. Very comfortable and the "
                               "pricing was transparent with no hidden charges."),
            ("Divya S.", 4, "Great experience overall. Driver knew all the local spots in Dhanushkodi. "
                             "Would book again for our next trip."),
        ]
        for i, (name, rating, text) in enumerate(reviews):
            ClientReview.objects.get_or_create(
                reviewer_name=name,
                defaults=dict(rating=rating, review_text=text, display_order=i, is_published=True)
            )
