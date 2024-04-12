import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from ..items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book_link in response.css(".product_pod a"):
            yield response.follow(book_link, callback=self.parse_book)

        # get next page and scrape it
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url)

    def parse_book(self, response):
        loader = ItemLoader(item=BookItem(), response=response)
        loader.default_output_processor = TakeFirst()

        # populate item using loader
        loader.add_css("title", "h1::text")
        loader.add_css("category", "ul.breadcrumb > li:nth-child(3) > a::text")
        loader.add_css("price", ".price_color::text")
        loader.add_css("rating", ".star-rating::attr(class)")
        loader.add_xpath(
            "availability",
            "//th[contains(text(), 'Availability')]/following-sibling::td/text()",
        )
        loader.add_xpath(
            "upc",
            "//th[contains(text(), 'UPC')]/following-sibling::td/text()",
        )
        loader.add_xpath(
            "tax",
            "//th[contains(text(), 'Tax')]/following-sibling::td/text()",
        )
        loader.add_xpath(
            "reviews_count",
            "//th[contains(text(), 'Number of reviews')]/following-sibling::td/text()",
        )
        loader.add_css("image_urls", "div.thumbnail img::attr(src)")

        yield loader.load_item()
