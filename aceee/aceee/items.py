# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AceeeItem(scrapy.Item):
    HEADER = scrapy.Field() # "Article's title" - Заголовок
    PUBDATE = scrapy.Field() # "2001-12-24" - Дата публикации
    CATEGORIES = scrapy.Field() # ["marketing", "sales"] - Категории (обычно это раздел на сайте). Если их нет, можно оставить этот блок пустым
    ARTICLE_TEXT = scrapy.Field() # Текст публикации, без кусков кода javascript, блоков рекламы и т.п.
    TAGS = scrapy.Field() # ["lorem", "ipsum"] - Теги - обычно идут внизу страницы, часто начинаются с символа "#". Могут быть не на всех страницах. Например, здесь есть: https://aceee.org/blog/2019/07/hot-enough-you-utilities-need, а на соседних страницах нет.
    HYPERLINKS = scrapy.Field() # ["http://bbc.com/important-article", "http://times.com/important-article"] # Cсылки на другие сайты

