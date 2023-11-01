# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from itemadapter import ItemAdapter


class AlmeeraPipeline():
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        item_data=dict(item)

        if 'image_urls' in item_data:
            del item_data['image_urls']
        self.items.append(item_data)
        return item

    def close_spider(self, spider):


        with open('output.json', 'w') as f:
            json.dump(self.items, f,indent=4)
