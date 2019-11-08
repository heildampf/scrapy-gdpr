# -*- coding: utf-8 -*-

# Copyright Christopher S. Penn, 2016 | cspenn.com | @cspenn
# This software is licensed under the GNU General Public License, version 3.0.
# Absolutely no warranty or support is provided.
# Run at your own risk.

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from TagChecker.items import TagcheckerItem

class TagSpider(CrawlSpider):
    name = "TagSpider"
    allowed_domains = ["christopherspenn.com"]
    start_urls = ['http://www.christopherspenn.com/']
    
    rules = (
        Rule(LinkExtractor(allow=r'/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        # Create an item and set some defualts 
        i = TagcheckerItem()
        i['url'] = response.url
        i['hasUniversal'] = '0'
        i['hasClassic'] = '0'
        i['hasTagManager'] = '0'

        # Check for classic
        sel = Selector(response)
        gaq = sel.xpath('//script[contains(., "google-analytics.com/ga.js")]')

        for js in gaq:
            i['hasClassic'] = '1'

        # Check for universal
        ga = sel.xpath('//script[contains(., "google-analytics.com/analytics.js")]')

        for js in ga:
            i['hasUniversal'] = '1'
            
        # Check for Tag Manager
        sel = Selector(response)
        gtm = sel.xpath('//script[contains(., "googletagmanager.com/gtm.js")]')

        for js in gtm:
            i['hasTagManager'] = '1'

        return i
