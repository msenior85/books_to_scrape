BOT_NAME = "books_project"

SPIDER_MODULES = ["books_project.spiders"]
NEWSPIDER_MODULE = "books_project.spiders"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

# Ignore robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    "books_project.pipelines.SQLiteDBPipeline": 300,
    "books_project.pipelines.BooksImagesPipeline": 400,
}

# location for saved images
IMAGES_STORE = "images"

# DATABASE CONNECTION URI
DATABASE_URI = "sqlite.db"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
