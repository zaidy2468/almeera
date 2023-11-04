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

        if 'image_urls' in item:
            del item['image_urls']
        item_data=item
        #Structuring the data in desired json format
        item_data1={
            "category_name":item_data.get('category_name'),
            "category_img_url":item_data.get('category_img_url'),
            "Subcategories" : [{
                "subcategory_name":item_data.get('subcategory_name'),
                "Products":item_data.get('products')

            }]
        }

        # making key for populating the products accoridng to their categories
        category_name = item_data1.get('category_name')
        subcategory_name = item_data1['Subcategories'][0].get('subcategory_name')
        key = (category_name, subcategory_name)

        index_to_update=None
        index1_to_update=None

        for index, entry in enumerate(self.items):
            entry_category_name=entry.get('category_name')
            entry_subcategory_name=entry['Subcategories'][0].get('subcategory_name')
            if (entry_category_name,entry_subcategory_name)==key:
                index_to_update=index

            elif entry_category_name==category_name:
                index1_to_update=index


        if index1_to_update is not None:
            self.items[index1_to_update]['Subcategories'].extend(item_data1['Subcategories'])

        elif index_to_update is not None:
            self.items[index_to_update]["Subcategories"][0]["Products"].extend(
                item_data.get('products'))

        # Handle the case where the key doesn't exist, such as creating a new entry
        else:
            self.items.append(item_data1)
        return self.items


    def close_spider(self, spider):
    # cleaning the data , checking for duplicate subcategories
        for itms in self.items:
            seen_subcategory_names = set()
            subcategories_to_remove = []

            # Iterate through subcategories and identify duplicates
            for subcategory in itms['Subcategories']:
                if subcategory['subcategory_name'] not in seen_subcategory_names:
                    seen_subcategory_names.add(subcategory['subcategory_name'])
                else:
                    subcategories_to_remove.append(subcategory)

            # Remove the duplicate subcategories from the main list
            itms['Subcategories'] = [subcategory for subcategory in itms['Subcategories'] if
                                     subcategory not in subcategories_to_remove]

        # Now, self.items contains the updated list with duplicate subcategories removed

        with open('output.json', 'w') as f:
            json.dump(self.items, f,indent=4)
