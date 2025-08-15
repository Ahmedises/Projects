import scrapy
from watch.items import WatchItem

class DetailsSpider(scrapy.Spider):
    name = "details"
    allowed_domains = ["egywatch.com"]
    start_urls = ["https://egywatch.com/collections/watches"]

    def parse(self, response):
        watches = response.css('div.collection__main div.product-wrap')
        watch_item = WatchItem()

        for watch in watches:
            relative_url = watch.css('div.product-thumbnail a').attrib['href']
            real_url = "https://egywatch.com/" + relative_url
            yield response.follow(real_url, callback=self.parse_details)


        next_page = response.xpath("//ul[@class = 'pagination-list']/following-sibling::a").attrib['href']
        if next_page is not None:
            real_next_page  = "https://egywatch.com/" + next_page
            yield response.follow(real_next_page, callback=self.parse)



    def parse_details(self, response):
        watch_item = WatchItem()
        details = response.css('div.product_section')
        spec = details.css('ul.tabs-content li#tab2')

        watch_item['name']  = details.css('div.product__information div h1.product_name.title::text').get()
        watch_item['price'] = details.css('div.product__information div span.current_price span::text').get() # has to be striped
        watch_item['reference_number'] = spec.css('div.custom-field__reference-number span.custom-field--value ::text').get() #has to be striped
        watch_item['brand'] = spec.css('div.custom-field__brand span.custom-field--value ::text').get()
        watch_item['series'] = spec.css('div.custom-field__series span.custom-field--value ::text').get()
        watch_item['movement'] = spec.css('div.custom-field__movement span.custom-field--value ::text').get()
        watch_item['case_material'] = spec.css('div.custom-field__case-material span.custom-field--value ::text').get()
        watch_item['strap_material'] = spec.css('div.custom-field__strap-material span.custom-field--value ::text').get()
        watch_item['gender'] = spec.css('div.custom-field__gender span.custom-field--value ::text').get()
        watch_item['glass'] = spec.css('div.custom-field__glass span.custom-field--value ::text').get()
        watch_item['water_resistance'] = spec.css('div.custom-field__water-resistance span.custom-field--value ::text').get()
        watch_item['made_in'] = spec.css('div.custom-field__made-in span.custom-field--value ::text').get()

        yield watch_item



