import re
from typing import Optional
from urllib.parse import urljoin

import scrapy
from itemloaders.processors import Identity, MapCompose

RATINGS_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
PATTERN = r"(\d+)"


def make_fullurl(value: str) -> str:
    url = urljoin("https://books.toscrape.com/", value)
    return url


def format_rating(value: str) -> Optional[int]:
    rating_str = value.split(" ")
    if rating_str:
        rating = RATINGS_MAP[rating_str[-1]]
        return rating
    rating = None


def format_reviews(value: str) -> Optional[int]:
    try:
        review_count = int(value)
    except ValueError:
        review_count = None
    return review_count


def format_availability(value: str) -> Optional[int]:
    match = re.search(PATTERN, value)
    if match:
        number_available = match.group(1)
        return int(number_available)
    return None


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    tax = scrapy.Field()
    rating = scrapy.Field(input_processor=MapCompose(format_rating))
    availability = scrapy.Field(input_processor=MapCompose(format_availability))
    upc = scrapy.Field()
    reviews_count = scrapy.Field(input_processor=MapCompose(format_reviews))
    image_urls = scrapy.Field(
        input_processor=MapCompose(make_fullurl),
        output_processor=Identity(),
    )
    images = scrapy.Field(output_processor=Identity())
