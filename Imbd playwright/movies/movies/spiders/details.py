import scrapy
from scrapy_playwright.page import PageMethod
from movies.items import MoviesItem
class DetailsSpider(scrapy.Spider):
    name = "details"
    allowed_domains = ["www.imdb.com"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,  # عشان تشوف اللي بيحصل
        }}

    def start_requests(self):
        custom_headers = {
            'Accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'Sec-fetch-user': '?1' ,
            'Sec-fetch-mode' : 'navigate',
            'Sec-fetch-Dest' : 'document',
            'Sec-fetch-site': 'same-origin' ,
            'Sec-ch-ua-platform': 'Windows',
            'Sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests' : '1',
            'Cookie' : 'session-id=146-2078274-8232322; session-id-time=2082787201l; ubid-main=134-5024321-8720501; ad-oo=0; ci=eyJpc0dkcHIiOmZhbHNlfQ; session-token=AxcUvEm4rc1jmptcxxctSG/KAnyJvO26PuF97EC+/lUypQ3VxU07wJTQVdYVg/ZzvN5PlfuPlQcoGc0kFhGKCpYnz2Y07iZvvEZekg5bUp/PPqd1mfPZEw/uo9faL+vjD2l/SFrk7nV+8yq4ZdK2CU5VHoNfubs9sM75RrenKzSYwq/IXLOCxIf8uA6ykionmkmGjC9IAJjUMyxDupItLLz9CwlEXrOKKPe1OV4y5mkhR+YXYlS4ht32VeIqPYSyPWOCpIKcqj8J56Qa7Mc81/gveO051QQEUEt3NMkKFArzYbZ/YrnBGdo1oGyK39ZH1Rh8auWW8jrTVnIvaGETEKkNCeTz0D07; csm-hit=tb:QVWTQDYN1YKJ27WVPVHH+s-H7PZTZCC093EFSJEZYZD|1754903800710&t:1754903800710&adb:adblk_yes',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",

        }
        url = "https://www.imdb.com/chart/top/?ref_=hm_nv_menu"
        yield scrapy.Request(url=url, callback=self.parse, meta = dict(
            playwright=True,
            playwright_include_page=True,
            playwright_args={"headless": False},
            playwright_page_method=[
                PageMethod("wait_for_selector", "li.ipc-metadata-list-summary-item"),
                PageMethod("wait_for_load_state", "networkidle"),
                PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod("wait_for_selector", "li.ipc-metadata-list-summary-item:nth-child(250)"),  # 10 per page
            ],
            errback=self.errback
        ))
    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.screenshot(path="imdb.png")
        details = await page.query_selector_all("li.ipc-metadata-list-summary-item")
        for detail in details:
            film_code = await detail.query_selector("a.ipc-title-link-wrapper")
            href = await film_code.get_attribute("href") if film_code else None
            link = "https://www.imdb.com/" + href
            if href:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_movie,
                    meta=dict(
                        playwright =  True,
                        playwright_include_page = True,
                        playwright_args={"headless": False},
                        film_link = link
                )
                )

        await page.close()
    async def parse_movie(self,response):
        page = response.meta["playwright_page"]
        await page.wait_for_selector('span.hero__primary-text[data-testid="hero__primary-text"]')
        # Director(s)
        director_elements = await page.query_selector_all(
            'li[data-testid="title-pc-principal-credit"]:has-text("Director") a'
        )
        directors = [await el.inner_text() for el in director_elements]
        # Writer(s)
        writer_elements = await page.query_selector_all(
            'li[data-testid="title-pc-principal-credit"]:has-text("Writers") a'
        )
        writers = [await el.inner_text() for el in writer_elements]

        # Star(s)
        star_elements = await page.query_selector_all(
            'li[data-testid="title-pc-principal-credit"]:has-text("Stars") a[href*="/name/"]'
        )
        stars = [await el.inner_text() for el in star_elements]

        # Movie name
        name = await page.query_selector('span.hero__primary-text[data-testid="hero__primary-text"]')
        name_text = await name.inner_text() if name else None

        # Rating
        rating_element = await page.query_selector('span.sc-4dc495c1-1.lbQcRY')
        rating = [await rating_element.inner_text() if rating_element else None]

        # Meta score
        meta_element = await page.query_selector('span.score span')
        meta_score =  await meta_element.inner_text() if meta_element else None

        # Tags
        tag_element = await page.query_selector_all('span.ipc-chip__text')
        tag = [await el.inner_text() for el in tag_element]

        # Preview
        preview_element = await page.query_selector('span.sc-bf30a0e-2.bRimta')
        preview = await preview_element.inner_text() if preview_element else None

        # Year
        Year_element = await page.query_selector('a.ipc-link.ipc-link--baseAlt.ipc-link--inherit-color')
        year = await Year_element.inner_text() if Year_element else None

        # # Image link
        # image_element = await page.query_selector('a.ipc-lockup-overlay.ipc-focusable')
        # image = await image_element.get_attribute("href") if image_element else None
        # if image:
        #     image_link = "https://www.imdb.com" + image
        # else:
        #     image_link = None
        #


        await page.close()
        # Returned items
        movie_items = MoviesItem()
        movie_items["Movie"] = name_text
        movie_items["Directors"] = directors
        movie_items["Writers"] = writers
        movie_items["Stars"] = stars
        movie_items["Link"] = response.meta.get("film_link")
        movie_items["Rating"] = rating
        movie_items["Meta_score"] = meta_score
        movie_items["Tags"] = tag
        movie_items["Preview"] = preview
        movie_items["Year"] = year
        # movie_items["Image"] = image_link
        yield movie_items


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

