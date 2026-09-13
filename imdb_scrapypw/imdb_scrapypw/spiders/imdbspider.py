from ast import parse
from time import sleep

import scrapy
from scrapy_playwright.page import PageMethod


class ImdbspiderSpider(scrapy.Spider):
    name = "imdbspider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/"]

    async  def start(self):
        url = "https://www.imdb.com/"
        yield scrapy.Request(
            url=url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_context_kwargs": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                    "viewport": {"width": 1920, "height": 1080},
                    "locale": "en-US"
                },
                "playwright_navigation_kwargs": {
                    "wait_until": "domcontentloaded",
                    "timeout": 60000,  # 60 seconds
                },
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "a.ipc-lockup-overlay"),
                ],
            },
            headers={
                "Accept-Language": "en-US,en;q=0.9",
            },
            callback=self.parse
        )
    async def parse(self, response):
        page = response.meta["playwright_page"]
        try:
            button = page.locator("button#suggestion-search-button")
            await button.click()
            sleep(10)
        finally:
            await page.close()
