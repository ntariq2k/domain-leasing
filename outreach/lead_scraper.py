"""
lead_scraper.py — scrapes local business leads from Google Maps Places API.
Usage: python outreach/lead_scraper.py
Output: outreach/leads.json

Requires: GOOGLE_MAPS_API_KEY env var
Free tier: $200/month credit (~3,300 nearby-search calls or ~1,100 detail calls/month)
"""
import os, json, time, urllib.request, urllib.parse

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

# Queries mapped to each domain — businesses most likely to want that website
DOMAIN_TARGETS = {
    "nycreagent.com":        ("real estate agent",          "New York, NY"),
    "webuyqueens.com":       ("real estate investor",       "Queens, NY"),
    "webuynycbuilding.com":  ("commercial real estate",     "New York, NY"),
    "webuynycbuildings.com": ("property management company","New York, NY"),
    "njsellersagent.com":    ("real estate agent",          "Newark, NJ"),
    "nycroofexperts.com":    ("roofing contractor",         "New York, NY"),
    "nycpaintexperts.com":   ("painting contractor",        "New York, NY"),
    "nycreconsultant.com":   ("real estate consultant",     "New York, NY"),
    "nycreconsultants.com":  ("real estate consulting firm","New York, NY"),
}

FIELDS = "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,email"


def geocode(location: str) -> dict | None:
    url = (
        "https://maps.googleapis.com/maps/api/geocode/json?address="
        + urllib.parse.quote(location)
        + "&key=" + API_KEY
    )
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)
    if data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return loc
    return None


def nearby_search(lat: float, lng: float, query: str, page_token: str = "") -> dict:
    params = {
        "location": f"{lat},{lng}",
        "radius": "10000",
        "keyword": query,
        "key": API_KEY,
    }
    if page_token:
        params["pagetoken"] = page_token
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)


def place_details(place_id: str) -> dict:
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json?place_id="
        + place_id
        + "&fields=name,formatted_address,formatted_phone_number,website,rating,user_ratings_total"
        + "&key=" + API_KEY
    )
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.load(r)
    return data.get("result", {})


def scrape_domain(domain: str, query: str, location: str, max_leads: int = 20) -> list:
    print(f"  [{domain}] Scraping '{query}' in {location}...")
    geo = geocode(location)
    if not geo:
        print(f"    Could not geocode {location}")
        return []

    leads = []
    page_token = ""
    seen = set()

    while len(leads) < max_leads:
        result = nearby_search(geo["lat"], geo["lng"], query, page_token)
        places = result.get("results", [])

        for place in places:
            if len(leads) >= max_leads:
                break
            place_id = place.get("place_id")
            if place_id in seen:
                continue
            seen.add(place_id)

            details = place_details(place_id)
            name    = details.get("name", place.get("name", ""))
            address = details.get("formatted_address", "")
            phone   = details.get("formatted_phone_number", "")
            website = details.get("website", "")
            rating  = details.get("rating", 0)
            reviews = details.get("user_ratings_total", 0)

            # Skip if they already have a strong website (not a placeholder)
            if website and not any(x in website.lower() for x in ["squarespace", "wix", "godaddy", "placeholder"]):
                has_site = True
            else:
                has_site = bool(website)

            leads.append({
                "domain": domain,
                "business_name": name,
                "address": address,
                "phone": phone,
                "website": website,
                "has_existing_site": has_site,
                "rating": rating,
                "review_count": reviews,
                "place_id": place_id,
            })
            time.sleep(0.1)  # stay under rate limits

        next_token = result.get("next_page_token")
        if not next_token or len(leads) >= max_leads:
            break
        page_token = next_token
        time.sleep(2)  # Google requires delay before using page token

    print(f"    Found {len(leads)} leads")
    return leads


def main():
    if not API_KEY:
        print("ERROR: Set GOOGLE_MAPS_API_KEY environment variable first.")
        print("Get a free key at: https://console.cloud.google.com/apis/library/places-backend.googleapis.com")
        return

    all_leads = []
    for domain, (query, location) in DOMAIN_TARGETS.items():
        leads = scrape_domain(domain, query, location, max_leads=20)
        all_leads.extend(leads)

    out_path = os.path.join(os.path.dirname(__file__), "leads.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_leads, f, indent=2, ensure_ascii=False)

    print(f"\nTotal leads scraped: {len(all_leads)}")
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
