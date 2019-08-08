import scrapy


class AceeeSpider(scrapy.Spider):
    name = 'aceee'
    start_urls = [
        'https://aceee.org/news-blog',
    ]

    def parse(self, response):
        for post in response.xpath('//div[@class="news-info-container clearfix"]/div[@class="news-content-box"]/h2/a/@href').extract():
            print('https://aceee.org' + post)
            