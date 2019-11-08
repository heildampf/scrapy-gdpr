""" A scrapy module to find things that might of of interest
    when implementing GDPR rules """

from urllib.parse import urlparse
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WebThing(scrapy.Item):
    """ An item to hold our data """
    t_type = scrapy.Field()
    page = scrapy.Field()
    f_id = scrapy.Field()
    name = scrapy.Field()
    action = scrapy.Field()
    inputs = scrapy.Field()


class GDPRAudit(CrawlSpider):
    """ Find things of interest to a GDPR audit """

    name = 'gdpr_audit'
    allowed_domains = None
    start_urls = None

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    out_filename = 'out.csv'
    out_file = None
    exporter = None

    def __init__(self, *args, **kwargs):
        super(GDPRAudit, self).__init__(*args, **kwargs)
        self.start_urls = open(self.urlfile, 'r').read().split('\n')
        self.allowed_domains = [urlparse(u)[1] for u in self.start_urls]
        print('ALLOWED DOMAINS: ' + ','.join(self.allowed_domains))

    def parse_item(self, response):
        

        frames = self.find_iframes(response)
        for frame in frames:
            yield frame

   
   
    def find_iframes(self, response):
        """ Look for iframes and collect some data about them """
        iframe_selector = '//script'
        for iframe in response.xpath(iframe_selector):
            frame_data = WebThing()
            frame_data['t_type'] = 'script'
            frame_data['page'] = response.request.url
            frame_data['action'] = iframe.xpath('@src').extract_first()
            yield frame_data
            
            
