from aceee.items import AceeeItem

import scrapy
import time


class AceeeSpider(scrapy.Spider):
    name = 'aceee'
    start_urls = ['https://aceee.org/news-blog', ]

    def parse(self, response):

        for post in response.xpath('''//div[@class="news-info-container clearfix"]
                                       /div[@class="news-content-box"]/h2/a/@href''').extract():
            yield response.follow('https://aceee.org' + post, callback = self.parse_post)
        
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        

    def parse_post(self, response):
        item = AceeeItem()

        HEADER = response.xpath('//h1[@class="inner-page-title"]/text()').extract()
        item['HEADER'] = HEADER


        PUBDATE = response.xpath('//div[@class="views-field views-field-created"]/span[@class="field-content"]/text()').get()

        if '|' in PUBDATE: # проверяю формат даты на странице и привожу его к общему виду
            date_list = PUBDATE.split()
            PUBDATE = ' '.join(date_list[1:4])

        date_obj = time.strptime(PUBDATE, "%B %d, %Y")
        item['PUBDATE'] = time.strftime("%Y-%m-%d", date_obj)


        # категория поста если она есть, указана первым тегом поста
        item['CATEGORIES'] = []


        ARTICLE_TEXT = ' '.join(response.xpath('//div[@class="new_content_body"]//text()').extract())
        item['ARTICLE_TEXT'] = ARTICLE_TEXT


        TAGS = response.xpath('//div[@class="views-field views-field-term-node-tid"]/span[@class="field-content"]//text()').extract()
        if TAGS:
            result = []
            for el in TAGS:
                if ',' not in el:
                    result.append(el)
            TAGS = result
        item['TAGS'] = TAGS


        HYPERLINKS = response.xpath('//div[@class="new_content_body"]//a/@href').extract()
        item['HYPERLINKS'] = HYPERLINKS
        
        yield item