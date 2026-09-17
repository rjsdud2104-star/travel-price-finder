"""Search orchestrator — filters hotels and attaches OTA prices."""
from __future__ import annotations
from datetime import datetime
from .mock_data import HOTELS, DESTINATIONS
from .providers.mock_provider import generate_prices
from .models import SearchRequest, SearchResponse, HotelResult, OTAPrice, Destination

FALLBACK_IMAGES = {
    "hotel":   "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=480&h=320&fit=crop",
    "resort":  "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=480&h=320&fit=crop",
    "pension": "https://images.unsplash.com/photo-1587061949409-02df41d5e562?w=480&h=320&fit=crop",
    "hostel":  "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=480&h=320&fit=crop",
}

def search(req: SearchRequest) -> SearchResponse:
    d1 = datetime.strptime(req.checkin, "%Y-%m-%d")
    d2 = datetime.strptime(req.checkout, "%Y-%m-%d")
    nights = max((d2 - d1).days, 1)

    candidates = [h for h in HOTELS if h["destination"] == req.destination]
    if not candidates:
        candidates = [h for h in HOTELS
                      if req.destination.lower() in h["destination"].lower()
                      or req.destination.lower() in h["name"].lower()]

    if req.hotel_type:
        candidates = [h for h in candidates if h["hotel_type"] == req.hotel_type]
    if req.min_rating:
        candidates = [h for h in candidates if h["rating"] >= req.min_rating]

    results: list[HotelResult] = []
    for h in candidates:
        prices_raw = generate_prices(h, req.checkin, req.checkout)
        if not prices_raw:
            continue
        prices = [OTAPrice(**p) for p in prices_raw]
        lowest = min(prices, key=lambda p: p.price)

        if req.min_price and lowest.price * nights < req.min_price:
            continue
        if req.max_price and lowest.price * nights > req.max_price:
            continue

        results.append(HotelResult(
            id=h["id"],
            name=h["name"],
            destination=h["destination"],
            category=h["category"],
            hotel_type=h["hotel_type"],
            rating=h["rating"],
            review_count=h["review_count"],
            image=h.get("image") or FALLBACK_IMAGES.get(h["hotel_type"], FALLBACK_IMAGES["hotel"]),
            address=h["address"],
            description=h["description"],
            amenities=h["amenities"],
            prices=[p.model_dump() for p in prices],
            lowest_price=lowest.price,
            lowest_provider=lowest.provider,
        ))

    sort_key = {
        "price": lambda r: r.lowest_price,
        "rating": lambda r: -r.rating,
        "name": lambda r: r.name,
    }.get(req.sort_by, lambda r: r.lowest_price)
    results.sort(key=sort_key)

    return SearchResponse(
        results=results,
        total=len(results),
        destination=req.destination,
        checkin=req.checkin,
        checkout=req.checkout,
        nights=nights,
    )

def get_destinations(category: str | None = None, q: str | None = None) -> list[Destination]:
    dests = DESTINATIONS
    if category:
        dests = [d for d in dests if d["category"] == category]
    if q:
        q_lower = q.lower()
        dests = [d for d in dests
                 if q_lower in d["name"].lower()
                 or q_lower in d["name_en"].lower()
                 or q_lower in d.get("country", "").lower()]
    return [Destination(**d) for d in dests]
