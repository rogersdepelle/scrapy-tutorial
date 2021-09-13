import scrapy


class BookSpider(scrapy.Spider):
    name = "books.toscrape.com"
    start_urls = ["http://books.toscrape.com/index.html"]

    def parse(self, response):
        books = response.css(".product_pod h3 a::attr(href)").extract()

        for book in books:
            yield response.follow(book, callback=self.parse_book)

        next_page = response.css(".next a::attr(href)").get()
        yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        item = {}
        item["title"] = response.css(".product_page h1::text").get()
        item["price"] = response.css(".product_page .price_color::text").get()
        item["description"] = response.css(".product_page > p::text").get()
        yield item
