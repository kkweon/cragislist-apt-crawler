# -*- coding: utf-8 -*-
import bs4
import requests
import scrapy
from scrapy.loader import ItemLoader

from craigslist_apt.items import CraigslistAptItem


class ClSpider(scrapy.Spider):
    name = "cl"
    allowed_domains = ["sfbay.craigslist.org"]
    # start_urls = (
    #     'http://sfbay.craigslist.org/search/apa',
    #     #'http://sfbay.craigslist.org/search/pen/apa?s=100',
    #     #https: // sfbay.craigslist.org / search / pen / apa?bedrooms = 1
    # )

    base_url = 'http://sfbay.craigslist.org'

    def start_requests(self):
        url = 'http://sfbay.craigslist.org/search/apa'#?s='
        first_page = requests.get(url).text
        html = bs4.BeautifulSoup(first_page, 'html.parser')
        total_count = html.find_all('span', {"class": "totalcount"})
        total_count = int(total_count[0].get_text())

        url_list = [url + "?s=" + str(i) for i in range(100, total_count, 100)]
        url_list.append(url)

        for url in url_list:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        link_list = response.xpath("//a[@class='hdrlnk']/@href").extract()  # /pen/apa/?????.html

        for i, link in enumerate(link_list):
            url = ClSpider.base_url + link
            item_loader = ItemLoader(item=CraigslistAptItem())
            item_loader.add_value('link', url)
            item_loader.add_value("area", url)
            request = scrapy.Request(url, self.parse_data)
            request.meta['item_loader'] = item_loader

            yield request

    def parse_data(self, response):
        # item meta
        # ===========
        # title,
        # price,
        # pub_date,
        # city,
        # link,
        # content,
        # address
        item_loader = response.meta['item_loader']
        title = response.xpath("//span[@id='titletextonly']/text()").extract()
        price = response.xpath("//span[@class='price']/text()").extract()
        house_type = response.xpath("//span[@class='housing']/text()").extract()  # '/ 3br - '
        city = response.xpath("//span[@class='postingtitletext']/small/text()").extract()
        pub_date = response.xpath("//time[@class='timeago']/@datetime").extract()[0]  # 2016-09-30T15:31-47-0700
        address = response.xpath("//div[@class='mapaddress']/text()").extract()

        item_loader.add_value('title', title)
        item_loader.add_value('price', price)
        item_loader.add_value('pub_date', pub_date)
        item_loader.add_value('city', city)
        item_loader.add_value('content', house_type)
        item_loader.add_value('bedroom', house_type)
        item_loader.add_value('size', house_type)
        item_loader.add_value('address', address)

        yield item_loader.load_item()
