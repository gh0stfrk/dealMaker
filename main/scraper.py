import scrapy
import json
import logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

class SinglePageSpider(scrapy.Spider):
    name = 'single_page_spider'

    def __init__(self, url=None, data_store=None, *args, **kwargs):
        super(SinglePageSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.data_store = data_store 

    def parse(self, response):
        script_tags = response.xpath('//script[@type="application/ld+json"]')
        for script_tag in script_tags:
            text = script_tag.xpath('./text()').get()
            if '"@type" : "Product"' in text:
                product_data = json.loads(text)
                # Store the extracted data in the external container
                self.data_store.append({
                    'name': product_data['name'],
                    'price': product_data['offers']['price'],
                    'url': response.url,
                    'image': product_data['image']
                })

def run_spider(url):
    logging.getLogger('scrapy').setLevel(logging.CRITICAL)
    scraped_data = []
    runner = CrawlerRunner(get_project_settings())
    
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(SinglePageSpider, url=url, data_store=scraped_data)
        reactor.stop()

    crawl()
    reactor.run()

    return scraped_data

if __name__ == '__main__':
    url = 'https://www.myntra.com/tshirts/articale/articale-men-black-solid-slim-fit-cotton-t-shirt/20697900/buy'
    data = run_spider(url)
    print(data)
