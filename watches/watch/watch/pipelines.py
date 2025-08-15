# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from os.path import join
import re

class WatchPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        fields_name = adapter.field_names()

        for field in fields_name:
            value = adapter.get(field)

            if value not in [None, '', ' ']:

                if field.lower() == "name":
                    value = re.sub(r'\s*-\s*', ' - ', value)
                    parts = value.split(' - ')
                    if len(parts) > 2:
                        clean_text = ' - '.join(parts[:2])
                    else:
                        clean_text = value
                    adapter[field] = clean_text.strip()
                    adapter['brand'] = parts[0].strip()
                # elif field.lower() == "brand":
                #     value = re.sub(r'\s*-\s*', ' - ', value)
                #     parts = value.split(' - ')
                #     adapter[field] = parts[0].strip()

                else:
                    clean_text = value.strip()
                    adapter[field] = clean_text

            else:
                if field == "gender":
                    adapter[field] = "Unisex"
                else:
                    adapter[field] = "Unknown"
        return item
