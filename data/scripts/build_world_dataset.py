"""
Build World Destinations Dataset
=================================
Creates a comprehensive world tourist destinations dataset.
Covers major attractions across all continents.
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)

WORLD_DESTINATIONS = [
    # === EUROPE ===
    {"place": "Eiffel Tower", "city": "Paris", "country": "France", "continent": "Europe", "category": "Landmark", "rating": 4.7, "best_time": "Apr-Jun, Sep-Oct", "avg_budget_usd": 150, "description": "Iconic iron lattice tower on the Champ de Mars. The most visited paid monument in the world with stunning city views.", "lat": 48.8584, "lng": 2.2945},
    {"place": "Colosseum", "city": "Rome", "country": "Italy", "continent": "Europe", "category": "Heritage", "rating": 4.8, "best_time": "Apr-Jun, Sep-Oct", "avg_budget_usd": 130, "description": "Ancient Roman amphitheatre, largest ever built. Symbol of Imperial Rome and one of the New Seven Wonders of the World.", "lat": 41.8902, "lng": 12.4922},
    {"place": "Santorini", "city": "Santorini", "country": "Greece", "continent": "Europe", "category": "Island", "rating": 4.8, "best_time": "Jun-Sep", "avg_budget_usd": 180, "description": "Stunning volcanic island with white-washed buildings, blue domes, and breathtaking sunsets over the Aegean Sea.", "lat": 36.3932, "lng": 25.4615},
    {"place": "Barcelona", "city": "Barcelona", "country": "Spain", "continent": "Europe", "category": "City", "rating": 4.6, "best_time": "May-Jun, Sep-Oct", "avg_budget_usd": 140, "description": "Gaudi's Sagrada Familia, Las Ramblas, Gothic Quarter, and beautiful beaches. Art, architecture, and Mediterranean vibes.", "lat": 41.3874, "lng": 2.1686},
    {"place": "Swiss Alps", "city": "Interlaken", "country": "Switzerland", "continent": "Europe", "category": "Nature", "rating": 4.9, "best_time": "Jun-Sep (summer), Dec-Mar (ski)", "avg_budget_usd": 250, "description": "Majestic mountain landscape with skiing, hiking, and scenic train rides. Jungfraujoch — Top of Europe.", "lat": 46.6863, "lng": 7.8632},
    {"place": "Amsterdam Canals", "city": "Amsterdam", "country": "Netherlands", "continent": "Europe", "category": "City", "rating": 4.5, "best_time": "Apr-May, Sep-Oct", "avg_budget_usd": 160, "description": "UNESCO World Heritage canal ring with museums (Van Gogh, Rijksmuseum), cycling culture, and tulip season.", "lat": 52.3676, "lng": 4.9041},
    {"place": "Plitvice Lakes", "city": "Plitvice", "country": "Croatia", "continent": "Europe", "category": "Nature", "rating": 4.8, "best_time": "Apr-Oct", "avg_budget_usd": 80, "description": "UNESCO World Heritage cascading lakes and waterfalls connected by wooden walkways through lush forest.", "lat": 44.8654, "lng": 15.5820},
    {"place": "Edinburgh Castle", "city": "Edinburgh", "country": "United Kingdom", "continent": "Europe", "category": "Heritage", "rating": 4.5, "best_time": "May-Sep", "avg_budget_usd": 140, "description": "Historic fortress dominating Edinburgh's skyline. Royal Mile, Arthur's Seat, and the famous Edinburgh Festival.", "lat": 55.9486, "lng": -3.1999},
    {"place": "Prague Old Town", "city": "Prague", "country": "Czech Republic", "continent": "Europe", "category": "Heritage", "rating": 4.6, "best_time": "Apr-Jun, Sep-Oct", "avg_budget_usd": 90, "description": "Fairy-tale medieval city with Charles Bridge, Astronomical Clock, and stunning Baroque architecture.", "lat": 50.0755, "lng": 14.4378},
    {"place": "Northern Lights", "city": "Tromsø", "country": "Norway", "continent": "Europe", "category": "Nature", "rating": 4.9, "best_time": "Sep-Mar", "avg_budget_usd": 200, "description": "Gateway to the Arctic for Aurora Borealis viewing. Dog sledding, whale watching, and midnight sun in summer.", "lat": 69.6492, "lng": 18.9553},
    {"place": "Amalfi Coast", "city": "Amalfi", "country": "Italy", "continent": "Europe", "category": "Coastal", "rating": 4.8, "best_time": "May-Sep", "avg_budget_usd": 200, "description": "UNESCO World Heritage dramatic coastline with colorful cliffside villages, crystal-clear waters, and Mediterranean cuisine.", "lat": 40.6340, "lng": 14.6027},
    {"place": "Istanbul", "city": "Istanbul", "country": "Turkey", "continent": "Europe", "category": "Heritage", "rating": 4.6, "best_time": "Apr-May, Sep-Nov", "avg_budget_usd": 80, "description": "Where East meets West — Hagia Sophia, Blue Mosque, Grand Bazaar, and Bosphorus strait connecting two continents.", "lat": 41.0082, "lng": 28.9784},

    # === ASIA (non-India) ===
    {"place": "Angkor Wat", "city": "Siem Reap", "country": "Cambodia", "continent": "Asia", "category": "Heritage", "rating": 4.8, "best_time": "Nov-Feb", "avg_budget_usd": 50, "description": "Largest religious monument in the world. Stunning 12th-century Khmer temple complex with iconic sunrise views.", "lat": 13.4125, "lng": 103.8670},
    {"place": "Great Wall", "city": "Beijing", "country": "China", "continent": "Asia", "category": "Heritage", "rating": 4.7, "best_time": "Apr-Jun, Sep-Nov", "avg_budget_usd": 80, "description": "Ancient fortification stretching 13,000 miles. Mutianyu and Badaling sections are most popular. One of the New Seven Wonders.", "lat": 40.4319, "lng": 116.5704},
    {"place": "Tokyo", "city": "Tokyo", "country": "Japan", "continent": "Asia", "category": "City", "rating": 4.7, "best_time": "Mar-May (cherry blossom), Oct-Nov", "avg_budget_usd": 150, "description": "Ultra-modern meets ancient Japan. Shibuya crossing, temples, anime culture, and world-class sushi.", "lat": 35.6762, "lng": 139.6503},
    {"place": "Bali", "city": "Bali", "country": "Indonesia", "continent": "Asia", "category": "Island", "rating": 4.6, "best_time": "Apr-Oct", "avg_budget_usd": 70, "description": "Island of the Gods with rice terraces, temples, beaches, yoga retreats, and vibrant nightlife in Seminyak.", "lat": -8.3405, "lng": 115.0920},
    {"place": "Ha Long Bay", "city": "Ha Long", "country": "Vietnam", "continent": "Asia", "category": "Nature", "rating": 4.7, "best_time": "Oct-Dec", "avg_budget_usd": 60, "description": "UNESCO World Heritage bay with thousands of limestone karsts and islands rising from emerald waters. Cruise paradise.", "lat": 20.9101, "lng": 107.1839},
    {"place": "Phuket", "city": "Phuket", "country": "Thailand", "continent": "Asia", "category": "Beach", "rating": 4.5, "best_time": "Nov-Apr", "avg_budget_usd": 60, "description": "Thailand's largest island with stunning beaches, vibrant nightlife, Thai temples, and island-hopping adventures.", "lat": 7.8804, "lng": 98.3923},
    {"place": "Petra", "city": "Wadi Musa", "country": "Jordan", "continent": "Asia", "category": "Heritage", "rating": 4.9, "best_time": "Mar-May, Sep-Nov", "avg_budget_usd": 100, "description": "Rose-red city carved into rock cliffs. UNESCO World Heritage and New Seven Wonders — the Treasury is iconic.", "lat": 30.3285, "lng": 35.4444},
    {"place": "Maldives", "city": "Malé", "country": "Maldives", "continent": "Asia", "category": "Island", "rating": 4.9, "best_time": "Nov-Apr", "avg_budget_usd": 300, "description": "Paradise overwater bungalows, crystal-clear lagoons, coral reefs, and bioluminescent beaches.", "lat": 4.1755, "lng": 73.5093},
    {"place": "Mount Fuji", "city": "Fujinomiya", "country": "Japan", "continent": "Asia", "category": "Nature", "rating": 4.6, "best_time": "Jul-Aug (climb), Year-round (view)", "avg_budget_usd": 120, "description": "Japan's iconic sacred mountain and highest peak. Climbing season in summer, stunning views from Lake Kawaguchi.", "lat": 35.3606, "lng": 138.7274},
    {"place": "Dubai", "city": "Dubai", "country": "UAE", "continent": "Asia", "category": "City", "rating": 4.5, "best_time": "Nov-Mar", "avg_budget_usd": 200, "description": "Futuristic city with Burj Khalifa, Palm Jumeirah, desert safaris, luxury shopping, and world-class entertainment.", "lat": 25.2048, "lng": 55.2708},

    # === AMERICAS ===
    {"place": "Machu Picchu", "city": "Cusco", "country": "Peru", "continent": "South America", "category": "Heritage", "rating": 4.9, "best_time": "May-Sep", "avg_budget_usd": 100, "description": "15th-century Inca citadel high in the Andes. One of the New Seven Wonders with breathtaking mountain views.", "lat": -13.1631, "lng": -72.5450},
    {"place": "Grand Canyon", "city": "Flagstaff", "country": "United States", "continent": "North America", "category": "Nature", "rating": 4.8, "best_time": "Mar-May, Sep-Nov", "avg_budget_usd": 120, "description": "Immense canyon carved by the Colorado River. South Rim views, hiking trails, and helicopter tours.", "lat": 36.1069, "lng": -112.1129},
    {"place": "New York City", "city": "New York", "country": "United States", "continent": "North America", "category": "City", "rating": 4.6, "best_time": "Apr-Jun, Sep-Nov", "avg_budget_usd": 250, "description": "The city that never sleeps — Statue of Liberty, Times Square, Central Park, Broadway, and world-class museums.", "lat": 40.7128, "lng": -74.0060},
    {"place": "Iguazu Falls", "city": "Foz do Iguaçu", "country": "Brazil", "continent": "South America", "category": "Nature", "rating": 4.9, "best_time": "Mar-May, Aug-Oct", "avg_budget_usd": 80, "description": "275 waterfalls spanning 1.7 miles on the Brazil-Argentina border. UNESCO World Heritage — more dramatic than Niagara.", "lat": -25.6953, "lng": -54.4367},
    {"place": "Cancún", "city": "Cancún", "country": "Mexico", "continent": "North America", "category": "Beach", "rating": 4.4, "best_time": "Dec-Apr", "avg_budget_usd": 120, "description": "Caribbean coast paradise with turquoise waters, Mayan ruins (Chichén Itzá nearby), cenotes, and vibrant nightlife.", "lat": 21.1619, "lng": -86.8515},
    {"place": "Galápagos Islands", "city": "Puerto Ayora", "country": "Ecuador", "continent": "South America", "category": "Wildlife", "rating": 4.9, "best_time": "Jun-Nov", "avg_budget_usd": 300, "description": "Living museum of evolution with unique wildlife — giant tortoises, marine iguanas, blue-footed boobies. Darwin's inspiration.", "lat": -0.7459, "lng": -90.3093},
    {"place": "Banff National Park", "city": "Banff", "country": "Canada", "continent": "North America", "category": "Nature", "rating": 4.8, "best_time": "Jun-Sep", "avg_budget_usd": 150, "description": "Turquoise glacial lakes (Lake Louise, Moraine Lake), Rocky Mountain landscapes, and abundant wildlife.", "lat": 51.4968, "lng": -115.9281},
    {"place": "Patagonia", "city": "El Calafate", "country": "Argentina", "continent": "South America", "category": "Nature", "rating": 4.8, "best_time": "Oct-Mar", "avg_budget_usd": 150, "description": "Rugged wilderness with Perito Moreno glacier, Torres del Paine, and dramatic Andean landscapes at the end of the world.", "lat": -50.3383, "lng": -72.2647},

    # === AFRICA ===
    {"place": "Serengeti Safari", "city": "Arusha", "country": "Tanzania", "continent": "Africa", "category": "Wildlife", "rating": 4.9, "best_time": "Jun-Oct", "avg_budget_usd": 250, "description": "World's greatest wildlife spectacle — the Great Migration of 2 million wildebeest. Big Five safaris.", "lat": -2.3333, "lng": 34.8333},
    {"place": "Pyramids of Giza", "city": "Cairo", "country": "Egypt", "continent": "Africa", "category": "Heritage", "rating": 4.7, "best_time": "Oct-Apr", "avg_budget_usd": 60, "description": "Last surviving Wonder of the Ancient World. The Great Sphinx and three pyramids — 4,500 years of history.", "lat": 29.9792, "lng": 31.1342},
    {"place": "Cape Town", "city": "Cape Town", "country": "South Africa", "continent": "Africa", "category": "City", "rating": 4.7, "best_time": "Nov-Mar", "avg_budget_usd": 100, "description": "Table Mountain, Cape of Good Hope, Robben Island, and wine country. Where mountains meet the ocean.", "lat": -33.9249, "lng": 18.4241},
    {"place": "Victoria Falls", "city": "Livingstone", "country": "Zambia", "continent": "Africa", "category": "Nature", "rating": 4.8, "best_time": "Feb-May", "avg_budget_usd": 120, "description": "The Smoke That Thunders — world's largest sheet of falling water on the Zambia-Zimbabwe border.", "lat": -17.9243, "lng": 25.8572},
    {"place": "Marrakech", "city": "Marrakech", "country": "Morocco", "continent": "Africa", "category": "Heritage", "rating": 4.5, "best_time": "Mar-May, Sep-Nov", "avg_budget_usd": 70, "description": "Vibrant medina with Jemaa el-Fnaa square, souks, palaces, and riads. Gateway to the Sahara Desert.", "lat": 31.6295, "lng": -7.9811},
    {"place": "Zanzibar", "city": "Stone Town", "country": "Tanzania", "continent": "Africa", "category": "Island", "rating": 4.5, "best_time": "Jun-Oct", "avg_budget_usd": 80, "description": "Spice Island with pristine white beaches, historic Stone Town (UNESCO), and turquoise Indian Ocean waters.", "lat": -6.1659, "lng": 39.2026},

    # === OCEANIA ===
    {"place": "Great Barrier Reef", "city": "Cairns", "country": "Australia", "continent": "Oceania", "category": "Nature", "rating": 4.8, "best_time": "Jun-Oct", "avg_budget_usd": 200, "description": "World's largest coral reef system. Snorkeling, diving among 1,500+ fish species and 400+ coral types.", "lat": -18.2871, "lng": 147.6992},
    {"place": "Sydney Opera House", "city": "Sydney", "country": "Australia", "continent": "Oceania", "category": "Landmark", "rating": 4.6, "best_time": "Sep-Nov, Mar-May", "avg_budget_usd": 180, "description": "UNESCO World Heritage architectural masterpiece on Sydney Harbour. Harbour Bridge, Bondi Beach, and coastal walks.", "lat": -33.8568, "lng": 151.2153},
    {"place": "Queenstown", "city": "Queenstown", "country": "New Zealand", "continent": "Oceania", "category": "Adventure", "rating": 4.8, "best_time": "Dec-Feb (summer), Jun-Aug (ski)", "avg_budget_usd": 180, "description": "Adventure capital of the world — bungee jumping, skydiving, jet boating. Stunning Milford Sound and Lord of the Rings scenery.", "lat": -45.0312, "lng": 168.6626},
    {"place": "Fiji Islands", "city": "Nadi", "country": "Fiji", "continent": "Oceania", "category": "Island", "rating": 4.7, "best_time": "May-Oct", "avg_budget_usd": 150, "description": "Tropical paradise with 333 islands, crystal lagoons, coral reefs, and the warmest people on Earth.", "lat": -17.7765, "lng": 177.9635},
]


def build_world_dataset():
    """Build and save the world destinations dataset."""
    print("Building world destinations dataset...")

    df = pd.DataFrame(WORLD_DESTINATIONS)

    # Rename columns for consistency
    df.columns = [
        "place_name", "city", "country", "continent", "category",
        "rating", "best_time_to_visit", "avg_budget_per_day_usd",
        "description", "latitude", "longitude"
    ]

    # Sort by continent then country
    df = df.sort_values(["continent", "country", "place_name"]).reset_index(drop=True)

    # Stats
    print(f"\n  Total destinations: {len(df)}")
    print(f"  Countries covered: {df['country'].nunique()}")
    print(f"  Continents: {df['continent'].nunique()}")
    print(f"\n  Continent distribution:")
    print(df["continent"].value_counts().to_string())
    print(f"\n  Category distribution:")
    print(df["category"].value_counts().to_string())

    # Save
    output_path = os.path.join(CLEANED_DIR, "destinations_world.csv")
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved to: {output_path}")

    return df


if __name__ == "__main__":
    build_world_dataset()
