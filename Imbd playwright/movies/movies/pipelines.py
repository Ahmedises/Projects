# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MoviesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        list_items = ["Directors", "Writers", "Stars","Tags"]
        for field_name in field_names:
            value = adapter.get(field_name)
            if value:
                if field_name in list_items:
                    value = adapter.get(field_name)
                    new_value = set(value)
                    adapter[field_name] = list(new_value)
                if field_name == "Tags" :
                    value = adapter.get("Tags")
                    new_value = value[:4]
                    adapter["Tags"] = new_value

            else:
                adapter[field_name] = "N/A"

        return item
