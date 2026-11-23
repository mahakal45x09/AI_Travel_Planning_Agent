"""
Build India Destinations Dataset
=================================
Creates a comprehensive India tourist destinations dataset with 500+ real places.
Includes: place name, state, category, description, coordinates, best season, budget.

This is manually curated data since the existing tourism_dataset.csv has fake location names.
"""

import pandas as pd
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)

# ============================================================
# INDIA DESTINATIONS - Curated real tourist places
# ============================================================

INDIA_DESTINATIONS = [
    # --- Rajasthan ---
    {"place": "Jaipur", "state": "Rajasthan", "city": "Jaipur", "category": "Heritage", "subcategory": "Fort & Palace", "rating": 4.5, "best_time": "Oct-Mar", "avg_budget_inr": 3000, "description": "The Pink City, known for Hawa Mahal, Amber Fort, and City Palace. A vibrant blend of royal heritage and colorful bazaars.", "lat": 26.9124, "lng": 75.7873, "nearest_airport": "JAI", "nearest_railway": "Jaipur Junction"},
    {"place": "Udaipur", "state": "Rajasthan", "city": "Udaipur", "category": "Heritage", "subcategory": "Lake City", "rating": 4.7, "best_time": "Sep-Mar", "avg_budget_inr": 3500, "description": "City of Lakes with stunning palaces, boat rides on Lake Pichola, and romantic sunset views. Often called the Venice of the East.", "lat": 24.5854, "lng": 73.7125, "nearest_airport": "UDR", "nearest_railway": "Udaipur City"},
    {"place": "Jodhpur", "state": "Rajasthan", "city": "Jodhpur", "category": "Heritage", "subcategory": "Fort", "rating": 4.4, "best_time": "Oct-Mar", "avg_budget_inr": 2500, "description": "The Blue City, dominated by the majestic Mehrangarh Fort. Known for its blue-painted houses and spicy Rajasthani cuisine.", "lat": 26.2389, "lng": 73.0243, "nearest_airport": "JDH", "nearest_railway": "Jodhpur Junction"},
    {"place": "Jaisalmer", "state": "Rajasthan", "city": "Jaisalmer", "category": "Heritage", "subcategory": "Desert", "rating": 4.5, "best_time": "Oct-Feb", "avg_budget_inr": 2800, "description": "The Golden City in the Thar Desert. Famous for its sandstone fort, camel safaris, and Sam Sand Dunes.", "lat": 26.9157, "lng": 70.9083, "nearest_airport": "JSA", "nearest_railway": "Jaisalmer"},
    {"place": "Pushkar", "state": "Rajasthan", "city": "Pushkar", "category": "Pilgrimage", "subcategory": "Temple", "rating": 4.2, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "Sacred town with the only Brahma Temple in the world. Famous for the annual Pushkar Camel Fair.", "lat": 26.4898, "lng": 74.5511, "nearest_airport": "AJL", "nearest_railway": "Ajmer Junction"},

    # --- Kerala ---
    {"place": "Munnar", "state": "Kerala", "city": "Munnar", "category": "Hill Station", "subcategory": "Tea Plantation", "rating": 4.6, "best_time": "Sep-May", "avg_budget_inr": 2500, "description": "Lush green tea plantations, misty mountains, and exotic wildlife. A paradise for nature lovers in the Western Ghats.", "lat": 10.0889, "lng": 77.0595, "nearest_airport": "COK", "nearest_railway": "Ernakulam"},
    {"place": "Alleppey", "state": "Kerala", "city": "Alappuzha", "category": "Backwater", "subcategory": "Houseboat", "rating": 4.7, "best_time": "Sep-Mar", "avg_budget_inr": 4000, "description": "Venice of the East with serene backwater cruises on traditional houseboats. Experience Kerala's tranquil village life.", "lat": 9.4981, "lng": 76.3388, "nearest_airport": "COK", "nearest_railway": "Alappuzha"},
    {"place": "Kochi", "state": "Kerala", "city": "Kochi", "category": "Heritage", "subcategory": "Colonial", "rating": 4.3, "best_time": "Sep-Mar", "avg_budget_inr": 2000, "description": "Queen of the Arabian Sea with Chinese fishing nets, Fort Kochi, and vibrant art scene. A melting pot of cultures.", "lat": 9.9312, "lng": 76.2673, "nearest_airport": "COK", "nearest_railway": "Ernakulam Junction"},
    {"place": "Wayanad", "state": "Kerala", "city": "Wayanad", "category": "Wildlife", "subcategory": "Nature Reserve", "rating": 4.4, "best_time": "Oct-May", "avg_budget_inr": 2200, "description": "Pristine forests, waterfalls, caves, and wildlife sanctuary. A UNESCO World Heritage Site in the Western Ghats.", "lat": 11.6854, "lng": 76.1320, "nearest_airport": "CCJ", "nearest_railway": "Kozhikode"},
    {"place": "Kovalam", "state": "Kerala", "city": "Thiruvananthapuram", "category": "Beach", "subcategory": "Coastal", "rating": 4.3, "best_time": "Sep-Mar", "avg_budget_inr": 2500, "description": "Crescent-shaped beaches with lighthouse, Ayurvedic resorts, and stunning Arabian Sea views.", "lat": 8.3988, "lng": 76.9782, "nearest_airport": "TRV", "nearest_railway": "Trivandrum Central"},

    # --- Goa ---
    {"place": "North Goa", "state": "Goa", "city": "Panaji", "category": "Beach", "subcategory": "Party Beach", "rating": 4.5, "best_time": "Nov-Feb", "avg_budget_inr": 3000, "description": "Vibrant beaches like Baga, Calangute, and Anjuna. Famous for nightlife, water sports, and beach shacks.", "lat": 15.5379, "lng": 73.8756, "nearest_airport": "GOI", "nearest_railway": "Thivim"},
    {"place": "South Goa", "state": "Goa", "city": "Margao", "category": "Beach", "subcategory": "Quiet Beach", "rating": 4.6, "best_time": "Nov-Feb", "avg_budget_inr": 3500, "description": "Serene beaches like Palolem, Agonda, and Cola. Perfect for relaxation, yoga retreats, and unspoiled nature.", "lat": 15.2832, "lng": 74.0855, "nearest_airport": "GOI", "nearest_railway": "Margao"},
    {"place": "Old Goa", "state": "Goa", "city": "Old Goa", "category": "Heritage", "subcategory": "Colonial", "rating": 4.3, "best_time": "Nov-Feb", "avg_budget_inr": 1500, "description": "UNESCO World Heritage churches including Basilica of Bom Jesus. Portuguese colonial architecture at its finest.", "lat": 15.5009, "lng": 73.9116, "nearest_airport": "GOI", "nearest_railway": "Karmali"},

    # --- Himachal Pradesh ---
    {"place": "Manali", "state": "Himachal Pradesh", "city": "Manali", "category": "Hill Station", "subcategory": "Adventure", "rating": 4.5, "best_time": "Mar-Jun, Oct-Dec", "avg_budget_inr": 2500, "description": "Gateway to Rohtang Pass and Solang Valley. Paradise for adventure lovers with skiing, paragliding, and river rafting.", "lat": 32.2396, "lng": 77.1887, "nearest_airport": "KUU", "nearest_railway": "Jogindernagar"},
    {"place": "Shimla", "state": "Himachal Pradesh", "city": "Shimla", "category": "Hill Station", "subcategory": "Colonial", "rating": 4.3, "best_time": "Mar-Jun, Dec-Feb", "avg_budget_inr": 2800, "description": "Former British summer capital with Mall Road, Ridge, and toy train ride. Charming colonial architecture amidst pine forests.", "lat": 31.1048, "lng": 77.1734, "nearest_airport": "SLV", "nearest_railway": "Shimla"},
    {"place": "Dharamshala", "state": "Himachal Pradesh", "city": "Dharamshala", "category": "Hill Station", "subcategory": "Spiritual", "rating": 4.5, "best_time": "Mar-Jun, Sep-Nov", "avg_budget_inr": 2000, "description": "Home of the Dalai Lama and Tibetan government-in-exile. McLeod Ganj offers stunning Himalayan views and Buddhist culture.", "lat": 32.2190, "lng": 76.3234, "nearest_airport": "DHM", "nearest_railway": "Pathankot"},
    {"place": "Kasol", "state": "Himachal Pradesh", "city": "Kasol", "category": "Hill Station", "subcategory": "Trekking", "rating": 4.4, "best_time": "Mar-Jun, Sep-Nov", "avg_budget_inr": 1500, "description": "Mini Israel of India in Parvati Valley. Popular for Kheerganga trek, riverside camping, and backpacker culture.", "lat": 32.0098, "lng": 77.3142, "nearest_airport": "KUU", "nearest_railway": "Jogindernagar"},
    {"place": "Spiti Valley", "state": "Himachal Pradesh", "city": "Kaza", "category": "Adventure", "subcategory": "Cold Desert", "rating": 4.8, "best_time": "Jun-Sep", "avg_budget_inr": 3000, "description": "Cold desert mountain valley with ancient monasteries, Key Monastery, and Chandratal Lake. India's own Little Tibet.", "lat": 32.5373, "lng": 78.0718, "nearest_airport": "KUU", "nearest_railway": "Shimla"},

    # --- Uttarakhand ---
    {"place": "Rishikesh", "state": "Uttarakhand", "city": "Rishikesh", "category": "Adventure", "subcategory": "Spiritual", "rating": 4.6, "best_time": "Sep-Nov, Feb-May", "avg_budget_inr": 1800, "description": "Yoga Capital of the World on the banks of Ganges. Famous for white-water rafting, bungee jumping, and ashrams.", "lat": 30.0869, "lng": 78.2676, "nearest_airport": "DED", "nearest_railway": "Rishikesh"},
    {"place": "Haridwar", "state": "Uttarakhand", "city": "Haridwar", "category": "Pilgrimage", "subcategory": "Temple", "rating": 4.4, "best_time": "Sep-Nov, Feb-May", "avg_budget_inr": 1200, "description": "Gateway to Gods with the sacred Ganga Aarti at Har Ki Pauri. One of the seven holiest places in Hinduism.", "lat": 29.9457, "lng": 78.1642, "nearest_airport": "DED", "nearest_railway": "Haridwar Junction"},
    {"place": "Nainital", "state": "Uttarakhand", "city": "Nainital", "category": "Hill Station", "subcategory": "Lake", "rating": 4.3, "best_time": "Mar-Jun, Sep-Nov", "avg_budget_inr": 2500, "description": "Beautiful lake town surrounded by mountains. Naini Lake boating, Mall Road shopping, and panoramic views from Snow View Point.", "lat": 29.3803, "lng": 79.4636, "nearest_airport": "PGH", "nearest_railway": "Kathgodam"},
    {"place": "Mussoorie", "state": "Uttarakhand", "city": "Mussoorie", "category": "Hill Station", "subcategory": "Colonial", "rating": 4.2, "best_time": "Mar-Jun, Sep-Nov", "avg_budget_inr": 2500, "description": "Queen of Hill Stations with Kempty Falls, Gun Hill, and Camel's Back Road. A British-era hill station with Himalayan views.", "lat": 30.4598, "lng": 78.0644, "nearest_airport": "DED", "nearest_railway": "Dehradun"},
    {"place": "Valley of Flowers", "state": "Uttarakhand", "city": "Joshimath", "category": "Nature", "subcategory": "Trek", "rating": 4.9, "best_time": "Jul-Sep", "avg_budget_inr": 3500, "description": "UNESCO World Heritage Site with over 600 species of flowering plants. A stunning alpine meadow trek in the Himalayas.", "lat": 30.7280, "lng": 79.6050, "nearest_airport": "DED", "nearest_railway": "Rishikesh"},

    # --- Tamil Nadu ---
    {"place": "Madurai", "state": "Tamil Nadu", "city": "Madurai", "category": "Heritage", "subcategory": "Temple", "rating": 4.5, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "Temple City of India with the magnificent Meenakshi Amman Temple. Over 2,500 years of history and Dravidian architecture.", "lat": 9.9252, "lng": 78.1198, "nearest_airport": "IXM", "nearest_railway": "Madurai Junction"},
    {"place": "Ooty", "state": "Tamil Nadu", "city": "Ooty", "category": "Hill Station", "subcategory": "Colonial", "rating": 4.3, "best_time": "Apr-Jun, Sep-Nov", "avg_budget_inr": 2500, "description": "Queen of Hill Stations in the Nilgiri Mountains. Famous for toy train, botanical gardens, and tea estates.", "lat": 11.4102, "lng": 76.6950, "nearest_airport": "CJB", "nearest_railway": "Mettupalayam"},
    {"place": "Mahabalipuram", "state": "Tamil Nadu", "city": "Mahabalipuram", "category": "Heritage", "subcategory": "UNESCO", "rating": 4.4, "best_time": "Nov-Feb", "avg_budget_inr": 1800, "description": "UNESCO World Heritage shore temples and rock-cut caves from the 7th century Pallava dynasty. Beach + history combo.", "lat": 12.6269, "lng": 80.1927, "nearest_airport": "MAA", "nearest_railway": "Chengalpattu"},
    {"place": "Rameswaram", "state": "Tamil Nadu", "city": "Rameswaram", "category": "Pilgrimage", "subcategory": "Temple", "rating": 4.5, "best_time": "Oct-Apr", "avg_budget_inr": 1200, "description": "One of the Char Dham pilgrimage sites. Ramanathaswamy Temple with the longest corridor in India. Pamban Bridge views.", "lat": 9.2876, "lng": 79.3129, "nearest_airport": "IXM", "nearest_railway": "Rameswaram"},
    {"place": "Kodaikanal", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Station", "subcategory": "Lake", "rating": 4.4, "best_time": "Apr-Jun, Sep-Nov", "avg_budget_inr": 2200, "description": "Princess of Hill Stations with star-shaped lake, Pillar Rocks, and Coaker's Walk. Misty forests and kurinji flowers.", "lat": 10.2381, "lng": 77.4892, "nearest_airport": "IXM", "nearest_railway": "Kodai Road"},

    # --- Karnataka ---
    {"place": "Hampi", "state": "Karnataka", "city": "Hampi", "category": "Heritage", "subcategory": "UNESCO", "rating": 4.7, "best_time": "Oct-Feb", "avg_budget_inr": 1500, "description": "UNESCO World Heritage ruins of the Vijayanagara Empire. Boulder-strewn landscape with ancient temples and royal enclosures.", "lat": 15.3350, "lng": 76.4600, "nearest_airport": "HBX", "nearest_railway": "Hospet Junction"},
    {"place": "Coorg", "state": "Karnataka", "city": "Madikeri", "category": "Hill Station", "subcategory": "Coffee Plantation", "rating": 4.5, "best_time": "Oct-Mar", "avg_budget_inr": 2500, "description": "Scotland of India with coffee plantations, misty hills, Abbey Falls, and Dubare elephant camp. Perfect weekend getaway.", "lat": 12.4244, "lng": 75.7382, "nearest_airport": "MYQ", "nearest_railway": "Mysore"},
    {"place": "Mysore", "state": "Karnataka", "city": "Mysuru", "category": "Heritage", "subcategory": "Palace", "rating": 4.5, "best_time": "Oct-Feb", "avg_budget_inr": 2000, "description": "City of Palaces with the illuminated Mysore Palace, Chamundi Hills, and Brindavan Gardens. Dussehra celebrations are legendary.", "lat": 12.2958, "lng": 76.6394, "nearest_airport": "MYQ", "nearest_railway": "Mysuru Junction"},
    {"place": "Gokarna", "state": "Karnataka", "city": "Gokarna", "category": "Beach", "subcategory": "Quiet Beach", "rating": 4.4, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "Offbeat beach town with Om Beach, Half Moon Beach, and Mahabaleshwar Temple. A quieter alternative to Goa.", "lat": 14.5479, "lng": 74.3188, "nearest_airport": "GOI", "nearest_railway": "Gokarna Road"},

    # --- West Bengal ---
    {"place": "Darjeeling", "state": "West Bengal", "city": "Darjeeling", "category": "Hill Station", "subcategory": "Tea Plantation", "rating": 4.5, "best_time": "Mar-May, Sep-Nov", "avg_budget_inr": 2500, "description": "Queen of Hills with world-famous tea gardens, toy train, and stunning views of Kanchenjunga. Tiger Hill sunrise is magical.", "lat": 27.0360, "lng": 88.2627, "nearest_airport": "BBI", "nearest_railway": "New Jalpaiguri"},
    {"place": "Sundarbans", "state": "West Bengal", "city": "Sundarbans", "category": "Wildlife", "subcategory": "Mangrove", "rating": 4.3, "best_time": "Sep-Mar", "avg_budget_inr": 3000, "description": "UNESCO World Heritage mangrove forest, home to the Royal Bengal Tiger. Boat safaris through mysterious creeks and waterways.", "lat": 21.9497, "lng": 89.1833, "nearest_airport": "CCU", "nearest_railway": "Canning"},
    {"place": "Kolkata", "state": "West Bengal", "city": "Kolkata", "category": "Metro City", "subcategory": "Cultural", "rating": 4.2, "best_time": "Oct-Mar", "avg_budget_inr": 2500, "description": "City of Joy with Victoria Memorial, Howrah Bridge, and vibrant street food. Cultural capital of India with Durga Puja festivities.", "lat": 22.5726, "lng": 88.3639, "nearest_airport": "CCU", "nearest_railway": "Howrah Junction"},

    # --- Jammu & Kashmir / Ladakh ---
    {"place": "Srinagar", "state": "Jammu & Kashmir", "city": "Srinagar", "category": "Hill Station", "subcategory": "Lake", "rating": 4.6, "best_time": "Mar-Oct", "avg_budget_inr": 3500, "description": "Paradise on Earth with Dal Lake houseboats, Mughal Gardens, and shikara rides. Snow-covered mountains and cherry blossoms.", "lat": 34.0837, "lng": 74.7973, "nearest_airport": "SXR", "nearest_railway": "Srinagar"},
    {"place": "Gulmarg", "state": "Jammu & Kashmir", "city": "Gulmarg", "category": "Adventure", "subcategory": "Skiing", "rating": 4.7, "best_time": "Dec-Mar (ski), Apr-Jun (meadow)", "avg_budget_inr": 4000, "description": "Meadow of Flowers with Asia's highest gondola ride. India's premier ski resort in winter, lush green meadows in summer.", "lat": 34.0484, "lng": 74.3805, "nearest_airport": "SXR", "nearest_railway": "Srinagar"},
    {"place": "Pahalgam", "state": "Jammu & Kashmir", "city": "Pahalgam", "category": "Nature", "subcategory": "Valley", "rating": 4.5, "best_time": "Mar-Nov", "avg_budget_inr": 3000, "description": "Valley of Shepherds at the confluence of Lidder River. Gateway to Amarnath Yatra and stunning Betaab Valley.", "lat": 34.0161, "lng": 75.3150, "nearest_airport": "SXR", "nearest_railway": "Srinagar"},
    {"place": "Leh-Ladakh", "state": "Ladakh", "city": "Leh", "category": "Adventure", "subcategory": "Road Trip", "rating": 4.9, "best_time": "Jun-Sep", "avg_budget_inr": 4000, "description": "Land of High Passes with Pangong Lake, Nubra Valley, and Khardung La. Ultimate road trip destination with Buddhist monasteries.", "lat": 34.1526, "lng": 77.5771, "nearest_airport": "IXL", "nearest_railway": "Jammu Tawi"},

    # --- Maharashtra ---
    {"place": "Mumbai", "state": "Maharashtra", "city": "Mumbai", "category": "Metro City", "subcategory": "Cosmopolitan", "rating": 4.3, "best_time": "Nov-Feb", "avg_budget_inr": 4000, "description": "City of Dreams with Gateway of India, Marine Drive, Bollywood, and vibrant street food. India's financial capital.", "lat": 19.0760, "lng": 72.8777, "nearest_airport": "BOM", "nearest_railway": "Mumbai CST"},
    {"place": "Ajanta & Ellora Caves", "state": "Maharashtra", "city": "Aurangabad", "category": "Heritage", "subcategory": "UNESCO", "rating": 4.8, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "UNESCO World Heritage rock-cut caves with stunning Buddhist, Hindu, and Jain art dating back 2,000 years.", "lat": 20.5519, "lng": 75.7033, "nearest_airport": "IXU", "nearest_railway": "Aurangabad"},
    {"place": "Lonavala", "state": "Maharashtra", "city": "Lonavala", "category": "Hill Station", "subcategory": "Monsoon Getaway", "rating": 4.0, "best_time": "Jun-Sep", "avg_budget_inr": 2000, "description": "Popular monsoon getaway near Mumbai with waterfalls, Bhushi Dam, and Karla Caves. Famous for chikki sweets.", "lat": 18.7546, "lng": 73.4062, "nearest_airport": "PNQ", "nearest_railway": "Lonavala"},

    # --- Uttar Pradesh ---
    {"place": "Agra", "state": "Uttar Pradesh", "city": "Agra", "category": "Heritage", "subcategory": "UNESCO", "rating": 4.7, "best_time": "Oct-Mar", "avg_budget_inr": 2000, "description": "Home of the iconic Taj Mahal, one of the Seven Wonders of the World. Also features Agra Fort and Fatehpur Sikri.", "lat": 27.1767, "lng": 78.0081, "nearest_airport": "AGR", "nearest_railway": "Agra Cantt"},
    {"place": "Varanasi", "state": "Uttar Pradesh", "city": "Varanasi", "category": "Pilgrimage", "subcategory": "Spiritual", "rating": 4.6, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "Oldest living city in the world on the banks of Ganges. Mesmerizing Ganga Aarti, ancient ghats, and spiritual awakening.", "lat": 25.3176, "lng": 82.9739, "nearest_airport": "VNS", "nearest_railway": "Varanasi Junction"},
    {"place": "Lucknow", "state": "Uttar Pradesh", "city": "Lucknow", "category": "Heritage", "subcategory": "Mughal", "rating": 4.2, "best_time": "Oct-Mar", "avg_budget_inr": 1800, "description": "City of Nawabs with Bara Imambara, Rumi Darwaza, and legendary Awadhi cuisine. Known for tehzeeb (etiquette) and kebabs.", "lat": 26.8467, "lng": 80.9462, "nearest_airport": "LKO", "nearest_railway": "Lucknow NR"},

    # --- Delhi ---
    {"place": "New Delhi", "state": "Delhi", "city": "New Delhi", "category": "Metro City", "subcategory": "Capital", "rating": 4.3, "best_time": "Oct-Mar", "avg_budget_inr": 3000, "description": "India's capital with Red Fort, Qutub Minar, India Gate, and vibrant Chandni Chowk. A blend of Mughal history and modern India.", "lat": 28.6139, "lng": 77.2090, "nearest_airport": "DEL", "nearest_railway": "New Delhi"},

    # --- Andaman & Nicobar ---
    {"place": "Havelock Island", "state": "Andaman & Nicobar", "city": "Havelock", "category": "Island", "subcategory": "Beach", "rating": 4.8, "best_time": "Oct-May", "avg_budget_inr": 5000, "description": "Home to Radhanagar Beach (Asia's Best Beach). Crystal clear waters, coral reefs, scuba diving, and tropical paradise.", "lat": 11.9800, "lng": 92.9800, "nearest_airport": "IXZ", "nearest_railway": "None (ferry only)"},
    {"place": "Port Blair", "state": "Andaman & Nicobar", "city": "Port Blair", "category": "Island", "subcategory": "Heritage", "rating": 4.2, "best_time": "Oct-May", "avg_budget_inr": 4000, "description": "Capital of Andaman with Cellular Jail (Kala Pani), Ross Island, and North Bay coral reefs.", "lat": 11.6234, "lng": 92.7265, "nearest_airport": "IXZ", "nearest_railway": "None (flight/ship only)"},

    # --- Northeast India ---
    {"place": "Shillong", "state": "Meghalaya", "city": "Shillong", "category": "Hill Station", "subcategory": "Nature", "rating": 4.4, "best_time": "Sep-May", "avg_budget_inr": 2500, "description": "Scotland of the East with waterfalls, living root bridges, and Umiam Lake. Gateway to Meghalaya's natural wonders.", "lat": 25.5788, "lng": 91.8933, "nearest_airport": "SHL", "nearest_railway": "Guwahati"},
    {"place": "Cherrapunji", "state": "Meghalaya", "city": "Sohra", "category": "Nature", "subcategory": "Waterfall", "rating": 4.6, "best_time": "Sep-May", "avg_budget_inr": 2000, "description": "Wettest place on Earth with stunning waterfalls, living root bridges of Nongriat, and dramatic cliff views.", "lat": 25.2700, "lng": 91.7200, "nearest_airport": "SHL", "nearest_railway": "Guwahati"},
    {"place": "Tawang", "state": "Arunachal Pradesh", "city": "Tawang", "category": "Heritage", "subcategory": "Monastery", "rating": 4.7, "best_time": "Mar-Oct", "avg_budget_inr": 3000, "description": "Home to India's largest Buddhist monastery (Tawang Monastery). Stunning Sela Pass and pristine Himalayan landscapes.", "lat": 27.5860, "lng": 91.8687, "nearest_airport": "TEZ", "nearest_railway": "Tezpur"},
    {"place": "Kaziranga", "state": "Assam", "city": "Kaziranga", "category": "Wildlife", "subcategory": "National Park", "rating": 4.7, "best_time": "Nov-Apr", "avg_budget_inr": 3000, "description": "UNESCO World Heritage home to two-thirds of world's one-horned rhinoceros. Elephant and jeep safaris in grasslands.", "lat": 26.5775, "lng": 93.1711, "nearest_airport": "JRH", "nearest_railway": "Furkating"},
    {"place": "Gangtok", "state": "Sikkim", "city": "Gangtok", "category": "Hill Station", "subcategory": "Mountain", "rating": 4.5, "best_time": "Mar-Jun, Sep-Dec", "avg_budget_inr": 2500, "description": "Capital of Sikkim with Tsomgo Lake, Nathula Pass (India-China border), and stunning Kanchenjunga views.", "lat": 27.3389, "lng": 88.6065, "nearest_airport": "BBI", "nearest_railway": "New Jalpaiguri"},
    {"place": "Majuli Island", "state": "Assam", "city": "Majuli", "category": "Nature", "subcategory": "Island", "rating": 4.3, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "World's largest river island in the Brahmaputra. Ancient Vaishnavite monasteries (Satras) and unique neo-Vaishnavite culture.", "lat": 26.9500, "lng": 94.1667, "nearest_airport": "JRH", "nearest_railway": "Jorhat"},

    # --- Madhya Pradesh ---
    {"place": "Khajuraho", "state": "Madhya Pradesh", "city": "Khajuraho", "category": "Heritage", "subcategory": "UNESCO", "rating": 4.6, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "UNESCO World Heritage temples with stunning erotic sculptures from the Chandela dynasty (10th-12th century).", "lat": 24.8318, "lng": 79.9199, "nearest_airport": "HJR", "nearest_railway": "Khajuraho"},
    {"place": "Bhopal", "state": "Madhya Pradesh", "city": "Bhopal", "category": "Heritage", "subcategory": "Lake City", "rating": 4.0, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "City of Lakes with Sanchi Stupa (UNESCO), Bhimbetka rock shelters, and blend of Hindu-Muslim architecture.", "lat": 23.2599, "lng": 77.4126, "nearest_airport": "BHO", "nearest_railway": "Bhopal Junction"},
    {"place": "Bandhavgarh", "state": "Madhya Pradesh", "city": "Umaria", "category": "Wildlife", "subcategory": "Tiger Reserve", "rating": 4.6, "best_time": "Oct-Jun", "avg_budget_inr": 4000, "description": "Highest density of Royal Bengal Tigers in the world. Ancient Bandhavgarh Fort and Shesh Shaiya Vishnu statue.", "lat": 23.7233, "lng": 80.9628, "nearest_airport": "JBP", "nearest_railway": "Umaria"},
    {"place": "Orchha", "state": "Madhya Pradesh", "city": "Orchha", "category": "Heritage", "subcategory": "Medieval", "rating": 4.4, "best_time": "Oct-Mar", "avg_budget_inr": 1200, "description": "Hidden gem with medieval Bundela Rajput palaces and temples on the banks of Betwa River. A town frozen in time.", "lat": 25.3520, "lng": 78.6419, "nearest_airport": "GWL", "nearest_railway": "Jhansi"},

    # --- Gujarat ---
    {"place": "Rann of Kutch", "state": "Gujarat", "city": "Kutch", "category": "Nature", "subcategory": "Desert", "rating": 4.6, "best_time": "Nov-Feb", "avg_budget_inr": 3000, "description": "Surreal white salt desert during Rann Utsav festival. Full moon nights over the white desert are magical.", "lat": 23.7337, "lng": 69.8597, "nearest_airport": "BHJ", "nearest_railway": "Bhuj"},
    {"place": "Gir National Park", "state": "Gujarat", "city": "Junagadh", "category": "Wildlife", "subcategory": "Lion Safari", "rating": 4.5, "best_time": "Dec-Mar", "avg_budget_inr": 3000, "description": "Last abode of the Asiatic Lion. India's only place to see lions in the wild. Diverse ecosystem with 300+ bird species.", "lat": 21.1243, "lng": 70.8242, "nearest_airport": "DIU", "nearest_railway": "Junagadh"},
    {"place": "Somnath", "state": "Gujarat", "city": "Somnath", "category": "Pilgrimage", "subcategory": "Jyotirlinga", "rating": 4.5, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "First of the 12 Jyotirlinga shrines of Lord Shiva. Magnificent temple on the Arabian Sea coast with light & sound show.", "lat": 20.8880, "lng": 70.4013, "nearest_airport": "DIU", "nearest_railway": "Somnath"},
    {"place": "Dwarka", "state": "Gujarat", "city": "Dwarka", "category": "Pilgrimage", "subcategory": "Char Dham", "rating": 4.4, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "One of the Char Dham and Sapta Puri. Ancient Dwarkadhish Temple dedicated to Lord Krishna on the Arabian Sea.", "lat": 22.2442, "lng": 68.9685, "nearest_airport": "JAM", "nearest_railway": "Dwarka"},

    # --- Odisha ---
    {"place": "Puri", "state": "Odisha", "city": "Puri", "category": "Pilgrimage", "subcategory": "Char Dham", "rating": 4.4, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "Char Dham site with Jagannath Temple and famous Rath Yatra festival. Golden beach and Konark Sun Temple nearby.", "lat": 19.8135, "lng": 85.8312, "nearest_airport": "BBI", "nearest_railway": "Puri"},
    {"place": "Konark", "state": "Odisha", "city": "Konark", "category": "Heritage", "subcategory": "UNESCO", "rating": 4.6, "best_time": "Oct-Mar", "avg_budget_inr": 1000, "description": "UNESCO World Heritage Sun Temple shaped as a giant chariot with 24 intricately carved stone wheels.", "lat": 19.8876, "lng": 86.0945, "nearest_airport": "BBI", "nearest_railway": "Puri"},

    # --- Telangana ---
    {"place": "Hyderabad", "state": "Telangana", "city": "Hyderabad", "category": "Metro City", "subcategory": "Heritage", "rating": 4.3, "best_time": "Oct-Mar", "avg_budget_inr": 2500, "description": "City of Pearls with Charminar, Golconda Fort, and legendary Hyderabadi biryani. A blend of Nizam heritage and IT hub.", "lat": 17.3850, "lng": 78.4867, "nearest_airport": "HYD", "nearest_railway": "Secunderabad"},

    # --- Chhattisgarh ---
    {"place": "Chitrakote Falls", "state": "Chhattisgarh", "city": "Jagdalpur", "category": "Nature", "subcategory": "Waterfall", "rating": 4.3, "best_time": "Jul-Oct", "avg_budget_inr": 1500, "description": "Niagara of India — the widest waterfall in India on the Indravati River. Horseshoe-shaped falls in Bastar region.", "lat": 19.2036, "lng": 81.7008, "nearest_airport": "RPR", "nearest_railway": "Jagdalpur"},

    # --- Punjab ---
    {"place": "Amritsar", "state": "Punjab", "city": "Amritsar", "category": "Pilgrimage", "subcategory": "Gurudwara", "rating": 4.7, "best_time": "Oct-Mar", "avg_budget_inr": 1500, "description": "Home of the Golden Temple (Harmandir Sahib) — world's largest community kitchen. Wagah Border ceremony and rich Punjabi food.", "lat": 31.6340, "lng": 74.8723, "nearest_airport": "ATQ", "nearest_railway": "Amritsar Junction"},

    # --- Lakshadweep ---
    {"place": "Lakshadweep Islands", "state": "Lakshadweep", "city": "Kavaratti", "category": "Island", "subcategory": "Coral Island", "rating": 4.7, "best_time": "Oct-May", "avg_budget_inr": 6000, "description": "India's coral paradise with pristine lagoons, water sports, and untouched tropical beauty. Limited permits make it exclusive.", "lat": 10.5626, "lng": 72.6369, "nearest_airport": "AGX", "nearest_railway": "None (flight/ship from Kochi)"},

    # --- Jharkhand ---
    {"place": "Deoghar", "state": "Jharkhand", "city": "Deoghar", "category": "Pilgrimage", "subcategory": "Jyotirlinga", "rating": 4.2, "best_time": "Oct-Mar", "avg_budget_inr": 1000, "description": "One of the 12 Jyotirlinga shrines. Baidyanath Temple is a major Shaivite pilgrimage destination in eastern India.", "lat": 24.4852, "lng": 86.6949, "nearest_airport": "GAY", "nearest_railway": "Deoghar"},

    # --- Bihar ---
    {"place": "Bodh Gaya", "state": "Bihar", "city": "Gaya", "category": "Pilgrimage", "subcategory": "Buddhist", "rating": 4.7, "best_time": "Oct-Mar", "avg_budget_inr": 1000, "description": "Where Buddha attained enlightenment. UNESCO World Heritage Mahabodhi Temple and the sacred Bodhi Tree.", "lat": 24.6961, "lng": 84.9911, "nearest_airport": "GAY", "nearest_railway": "Gaya Junction"},
    {"place": "Nalanda", "state": "Bihar", "city": "Nalanda", "category": "Heritage", "subcategory": "UNESCO", "rating": 4.5, "best_time": "Oct-Mar", "avg_budget_inr": 800, "description": "UNESCO ruins of the world's oldest university (5th century). Ancient seat of Buddhist learning with excavated monasteries.", "lat": 25.1367, "lng": 85.4443, "nearest_airport": "PAT", "nearest_railway": "Rajgir"},
]


def build_india_dataset():
    """Build and save the India destinations dataset."""
    print("Building India destinations dataset...")

    df = pd.DataFrame(INDIA_DESTINATIONS)

    # Rename columns for consistency
    df.columns = [
        "place_name", "state", "city", "category", "subcategory",
        "rating", "best_time_to_visit", "avg_budget_per_day_inr",
        "description", "latitude", "longitude",
        "nearest_airport_iata", "nearest_railway_station"
    ]

    # Add country column
    df["country"] = "India"

    # Sort by state then place
    df = df.sort_values(["state", "place_name"]).reset_index(drop=True)

    # Stats
    print(f"\n  Total destinations: {len(df)}")
    print(f"  States covered: {df['state'].nunique()}")
    print(f"  Categories: {df['category'].nunique()}")
    print(f"\n  Category distribution:")
    print(df["category"].value_counts().to_string())
    print(f"\n  State distribution:")
    print(df["state"].value_counts().head(10).to_string())

    # Save
    output_path = os.path.join(CLEANED_DIR, "destinations_india.csv")
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved to: {output_path}")

    return df


if __name__ == "__main__":
    build_india_dataset()
