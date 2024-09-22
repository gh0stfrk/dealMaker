import scrapy
import json


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["myntra.com"]

    def start_requests(self):
        # fetch the list of codes from the database
        items = [29951923, 30097171, 22183904]
        for code in items:
            url = f"https://www.myntra.com/{code}"
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        script_tags = response.xpath('//script[@type="application/ld+json"]')
        for script_tag in script_tags:
            text = script_tag.xpath('./text()').get()
            if '"@type" : "Product"' in text:
                product_data = json.loads(text)
                print(product_data)
                yield {
                    'name': product_data['name'],
                    'price': product_data['offers']['price'],
                    'url': response.url,
                    'image': product_data['image']
                }
