import logging
import scrapy
import sys
import re
import urllib.parse

from scrapy.crawler import CrawlerProcess
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

class ExtractSpider(scrapy.Spider):
    name = "numberlogo" 

    start_urls = [sys.argv[1]] 
       
    def parse(self, response):
        
        # returns phone numbers from href
        phone1 = response.xpath('//a[contains(@href, "http://+")]/text() | //a[contains(@href, "#")]/text() | //a[contains(@href, "tel")]/text()').re(r'.*\d')
        phone1 = list(set(phone1))
       
        #returns phone numbers from p tags in body of page
        phone2 = response.xpath('//p/text()').re(r'^[0-9+\(\)#\.\s\/ext-]+$')
        phone2=[''.join(re.findall('\d+', i)) for i in phone2]
        phone2 = [x for x in phone2 if x]
        phonenumbers=phone1+phone2
        
        if not phonenumbers:
            print('None')
        else: 
            print(phonenumbers)

        # Returns the logo
        logo = response.xpath('//img[contains(@class, "logo")]/@src | //img[contains(@src, "Logo")]/@src').get()
        logo = urllib.parse.urljoin(response.url, logo.strip())
        if not logo:
            print('None')
        else:
            print(logo)

        yield 
            

process = CrawlerProcess()
process.crawl(ExtractSpider)
process.start()

