from aceee.items import AceeeItem

import scrapy


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

        PUBDATE = response.xpath('//div[@class="views-field views-field-created"]/span[@class="field-content"]/text()').extract()
        item['PUBDATE'] = PUBDATE

        # CATEGORIES = response.xpath('//div[contains(@class, "col-sm-9")]/p/text()').extract()
        # item['CATEGORIES'] = CATEGORIES

        ARTICLE_TEXT = response.xpath('//div[@class="new_content_body"]//text()').extract()
        item['ARTICLE_TEXT'] = ARTICLE_TEXT

        # TAGS = response.xpath('//div[contains(@class, "col-sm-9")]/p/text()').extract()
        # item['TAGS'] = TAGS

        # HYPERLINKS = response.xpath('//div[contains(@class, "col-sm-9")]/p/text()').extract()
        # item['HYPERLINKS'] = HYPERLINKS
        
        yield item