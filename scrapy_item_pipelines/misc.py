from scrapy.exceptions import DropItem

from itemadapter import ItemAdapter


class FilterDuplicatesPipeline:
    """Scrapy Item Pipeline to drop duplicate items per spider run."""

    def __init__(self, *args, **kwargs):
        self.ids_seen = set()
        super().__init__(*args, **kwargs)

    def get_unique_value_from_item(self, item, keys):
        """Calculate a unique value from item using unique keys.
        Args:
            item(scrapy.Item instance)
            keys (tuple): Tuple of key representing unique key"""

        return "-".join(map(str, [item.get(k) for k in keys]))

    def process_item(self, item, spider):
        item_adapted = ItemAdapter(item)
        key_or_keys = getattr(item, "unique_key", "id")

        # To skip duplicate filterging define unique_key = None in item
        if key_or_keys is None:
            return item

        keys = key_or_keys if isinstance(key_or_keys, (tuple, list)) else (key_or_keys,)
        unique_value = self.get_unique_value_from_item(item_adapted, keys)
        if unique_value in self.ids_seen:
            spider.crawler.stats.inc_value("duplicate_item_count")
            duplicate_string = ", ".join([f"{k}: {item_adapted.get(k)}" for k in keys])
            raise DropItem(f"Duplicate item found: {duplicate_string}")
        else:
            self.ids_seen.add(unique_value)
            return item
