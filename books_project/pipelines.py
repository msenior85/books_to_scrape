import hashlib
import sqlite3
from copy import deepcopy

from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class SQLiteDBPipeline:
    def __init__(self, settings) -> None:
        self.SQLITE_DB = settings.get("DATABASE_URI")
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider) -> None:
        # create a database connection
        self.conn = sqlite3.connect(self.SQLITE_DB)
        spider.logger.info("Database connection opened.")

        # create a table in the database
        QUERY = """
            CREATE TABLE IF NOT EXISTS books(
                id integer primary key autoincrement,
                title text,
                category text,
                price text,
                tax text,
                rating integer,
                availability integer,
                upc text unique,
                reviews_count integer,
                image_urls text
            );
        """
        cur = self.conn.cursor()
        cur.execute(QUERY)
        cur.close()

    def spider_closed(self, spider) -> None:
        # close database connection
        self.conn.close()
        spider.logger.info("Database connection closed.")

    def process_item(self, item, spider):
        item_copy = deepcopy(item)
        adapter = ItemAdapter(item_copy)
        # convert image urls into one string separated by ~
        adapter["image_urls"] = "~".join(adapter.get("image_urls", []))

        cur = self.conn.cursor()
        try:
            cur.execute(
                """INSERT INTO books (title, category, price, tax, rating, 
                    availability, upc, reviews_count, image_urls) VALUES(
                        :title,
                        :category,
                        :price,
                        :tax,
                        :rating,
                        :availability,
                        :upc,
                        :reviews_count,
                        :image_urls)
                    """,
                adapter.asdict(),
            )
            self.conn.commit()
            id = cur.lastrowid
            item["id"] = id
            # print(item)
            spider.logger.info(
                f"<BookItem {id} {adapter.get('title')}> successfully inserted into database."
            )
        except Exception as err:
            # drop items that are not inserted into database
            raise DropItem(f"DB Error - {err}")
        finally:
            cur.close()
        return item


class BooksImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # create a shorter name to use for saving based on  database id and image url
        image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        return f"{item['id']}-{image_url_hash}.jpg"
