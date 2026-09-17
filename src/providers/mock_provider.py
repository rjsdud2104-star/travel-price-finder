"""Mock OTA provider — generates realistic price variations and real booking URLs."""
from __future__ import annotations
import hashlib, random
from urllib.parse import quote
from ..mock_data import OTA_PROVIDERS


def _seed(hotel_id: str, provider: str, checkin: str) -> int:
    h = hashlib.md5(f"{hotel_id}:{provider}:{checkin}".encode()).hexdigest()
    return int(h[:8], 16)


def _booking_url(provider: str, hotel_name: str, destination: str,
                 checkin: str, checkout: str) -> str:
    name = quote(hotel_name)
    dest = quote(destination)
    if provider == "야놀자":
        return f"https://www.yanolja.com/search/{name}"
    elif provider == "여기어때":
        return f"https://www.goodchoice.kr/product/search/2?keyword={name}"
    elif provider == "부킹닷컴":
        return (f"https://www.booking.com/searchresults.ko.html"
                f"?ss={name}&checkin={checkin}&checkout={checkout}")
    elif provider == "아고다":
        return (f"https://www.agoda.com/ko-kr/search"
                f"?textToSearch={name}&checkIn={checkin}&checkOut={checkout}")
    elif provider == "호텔스닷컴":
        return (f"https://kr.hotels.com/search.do"
                f"?q-destination={name}&q-check-in={checkin}&q-check-out={checkout}")
    elif provider == "트립닷컴":
        return (f"https://kr.trip.com/hotels/list"
                f"?keyword={name}&city={dest}&checkin={checkin}&checkout={checkout}")
    return f"https://www.google.com/search?q={name}+{dest}+호텔+예약"


def generate_prices(hotel: dict, checkin: str, checkout: str) -> list[dict]:
    base = hotel["base_price"]
    results = []
    for ota in OTA_PROVIDERS:
        rng = random.Random(_seed(hotel["id"], ota["name"], checkin))
        variation = rng.uniform(0.82, 1.18)
        price = int(base * variation / 1000) * 1000
        has_discount = rng.random() < 0.35
        original = int(price * rng.uniform(1.1, 1.3) / 1000) * 1000 if has_discount else None
        available = rng.random() < 0.88
        if not available:
            continue
        results.append({
            "provider": ota["name"],
            "price": price,
            "original_price": original,
            "url": _booking_url(ota["name"], hotel["name"], hotel["destination"],
                                checkin, checkout),
        })
    return sorted(results, key=lambda x: x["price"])
