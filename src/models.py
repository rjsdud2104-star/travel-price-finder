from __future__ import annotations
from pydantic import BaseModel

class SearchRequest(BaseModel):
    destination: str
    checkin: str          # YYYY-MM-DD
    checkout: str         # YYYY-MM-DD
    guests: int = 2
    category: str = "domestic"  # domestic | international
    sort_by: str = "price"      # price | rating | name
    min_price: int | None = None
    max_price: int | None = None
    hotel_type: str | None = None   # hotel | resort | pension | hostel
    min_rating: float | None = None

class OTAPrice(BaseModel):
    provider: str       # OTA name
    price: int          # per night, KRW
    url: str
    original_price: int | None = None  # before discount

class HotelResult(BaseModel):
    id: str
    name: str
    destination: str
    category: str
    hotel_type: str
    rating: float       # 0-5
    review_count: int
    image: str
    address: str
    description: str
    amenities: list[str]
    prices: list[OTAPrice]
    lowest_price: int
    lowest_provider: str

class SearchResponse(BaseModel):
    results: list[HotelResult]
    total: int
    destination: str
    checkin: str
    checkout: str
    nights: int

class Destination(BaseModel):
    name: str
    name_en: str
    category: str
    country: str
    popular: bool = False
