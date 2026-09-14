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
            await page.get_by_text("Movies, TV & more").click()
            title_accordion = page.get_by_test_id("accordion-item-titleTypeAccordion")
            if title_accordion.get_attribute("aria-label") == "Expand Title type":
                await title_accordion.click()
            movie_c = page.get_by_test_id("test-chip-id-movie")
            await movie_c.click()

            genre_accordion = page.get_by_test_id("accordion-item-genreAccordion")
            if await genre_accordion.get_attribute("aria-label") == "Expand Genre":
                await genre_accordion.click()
            comedy_c = page.get_by_test_id("test-chip-id-Comedy")
            await comedy_c.click()

            awards_accordion = page.get_by_test_id("accordion-item-awardsAccordion")
            if await awards_accordion.get_attribute("aria-label") == "Expand Awards & recognition":
                await awards_accordion.click()
            awards_b = page.get_by_test_id("test-chip-id-oscar-nominated")
            await awards_b.click()
            await page.get_by_test_id("adv-search-get-results").click()

            sleep(5)
        finally:
            await page.close()
