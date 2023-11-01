# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlmeeraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    category_name=scrapy.Field()
    category_img_url=scrapy.Field()
    subcategory_name=scrapy.Field()
    subcategory_img_url=scrapy.Field()
    products=scrapy.Field()
    image_urls = scrapy.Field()
    images=scrapy.Field()
    pass




