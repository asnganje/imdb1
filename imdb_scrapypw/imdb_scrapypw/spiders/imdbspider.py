from urllib.parse import urljoin

import scrapy
from scrapy_playwright.page import PageMethod
from ..items import MovieItem


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

            product_urls = await page.locator("div.ipc-title--title a").evaluate_all(
                "(elements)=>elements.map(el=>el.getAttribute('href'))")

            for i, product_url in enumerate(product_urls):
                product_url = urljoin(response.url, product_url)
                if i == 1:
                    break
                yield scrapy.Request(
                    product_url,
                    callback=self.parse_product,
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
                    }
                )

        finally:
            await page.close()
    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        try:
            movie_item = MovieItem()
            name = response.css("span[data-testid = 'hero__primary-text']::text").get()
            if not name:
                name = "No name"
            year = response.css("div.sc-dcbc0103-0.fRoBlK a.ipc-link::text").get()
            if not year:
                year = "No year"
            li_items = response.css("div.sc-dcbc0103-0.fRoBlK li.ipc-inline-list__item")
            duration = li_items[2].css("::text").get()
            if not duration:
                duration = "No duration"
            stars = response.css("div.sc-89427c75-3.foJWCy span.sc-a30a09c4-1.leFYws::text").get()
            if not stars:
                stars = "No stars"
            votes = response.css("div.sc-89427c75-3.foJWCy div.sc-a30a09c4-3.bhBkhl::text").get()
            if not votes:
                votes = "No votes"
            metascore = response.css("span.score span::text").get()
            if not metascore:
                metascore = "No metascore"

            description = response.css("section.sc-dcbc0103-4.cgzafN span[data-testid='plot-xl'] span[lang='en-US'] span::text").get()
            if not description:
                description = "No description"
            director = response.css("div.sc-dcbc0103-3.kizyQE li").xpath(".//*[contains(text(), 'Director')]/ancestor::li//a/text()").get()
            if not director:
                director = "No Director details"
            movie_item['name'] = name
            movie_item['year'] = year
            movie_item['duration'] = duration
            movie_item['stars'] = stars
            movie_item['votes'] = votes
            movie_item['metascore'] = metascore
            movie_item['description'] = description
            movie_item['director'] = director
            yield movie_item
        finally:
            await page.close()