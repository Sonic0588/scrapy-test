from aceee.items import AceeeItem

import scrapy
import time


class AceeeSpider(scrapy.Spider):
    name = 'aceee'
    start_urls = ['https://aceee.org/news-blog', ]
    #posts_urls = set()

    def parse(self, response):

        for post in response.xpath('''//div[@class="news-info-container clearfix"]
                                       /div[@class="news-content-box"]/h2/a/@href''').extract():

            #self.posts_urls.add('https://aceee.org' + post)
            yield response.follow('https://aceee.org' + post, callback = self.parse_post)
        
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        
    def parse_post(self, response):
        item = AceeeItem()

        HEADER = response.xpath('//h1[@class="inner-page-title"]/text()').extract()
        item['HEADER'] = HEADER

        PUBDATE = response.xpath('//div[@class="views-field views-field-created"]/span[@class="field-content"]/text()').get()

        if '|' in PUBDATE:
            date_str = PUBDATE[3:-10]
            print(date_str)
            date_obj = time.strptime(date_str, "%B %d, %Y")
        else:
            date_obj = time.strptime(PUBDATE, "%B %d, %Y")

        item['PUBDATE'] = time.strftime("%Y-%m-%d", date_obj)

        # CATEGORIES = response.xpath('//div[contains(@class, "col-sm-9")]/p/text()').extract()
        # item['CATEGORIES'] = CATEGORIES or []

        ARTICLE_TEXT = ' '.join(response.xpath('//div[@class="new_content_body"]//text()').extract())
        item['ARTICLE_TEXT'] = ARTICLE_TEXT

        TAGS = list(response.xpath('//div[@class="views-field views-field-term-node-tid"]/span[@class="field-content"]//text()').extract())
        item['TAGS'] = TAGS or []

        # HYPERLINKS = response.xpath('//div[contains(@class, "col-sm-9")]/p/text()').extract()
        # item['HYPERLINKS'] = HYPERLINKS or []
        
        yield item