# scrapy-item-pipelines

Various scrapy item pipelines

## Installation

pip install scrapy-item-pipelines

## SaveToKafkaPipeline

Item pipeline to push items to kafka. Items will be converted into JSON format and pushed to a defined kafka topic.


### Settings

```
SL_SCRAPY_ITEM_PIPELINES_SETTINGS = {
    "push_to_kafka_hosts": "localhost:9092"  # Kafka broker hosts. Separated with a comma.
    "push_to_kafka_default_topic": ""  # kafka default topic.
}
```


### Usage

If items should be pushed to different kafka topics per item, the topic can be defined in the item class.
Also if a data key should be pushed to kafka we can define the item field value to use by defining it
in the item class. If no `kafka_data_key` is defined no data key will be pushed.

```
class DemoItem(scrapy.Item):
    kafka_topic = "topic-to-push-items"
    kafka_data_key = "another_unique_field"

    field_name = scrapy.Field()
    another_unique_field = scrapy.Field()
```

After configuring add `scrapy_item_pipelines.streaming.PushToKafkaPipeline` to the ITEM_PIPELINES setting.

```
ITEM_PIPELINES = {
    ...
    ...
    "scrapy_item_pipelines.streaming.PushToKafkaPipeline": 999,
}
```

## FilterDuplicatesPipeline

Item pipeline to filter out duplicate items calculated using defined keys in the item.

### Usage

Define an attribute called unique_key in the item. If the unique key is a single field
unique_key can be defined as a string or if the unique key is a multi field key unique_key
should be a tuple of strings. If no unique_key is defined filtering will be done `id` field.
If you want to skip duplicate filtering for an item define unique_key as None.

The pipeline will include a stats called `duplicate_item_count` which is the number
of duplicate items dropped.

```
class DemoItem(scrapy.Item):
    field1 = scrapy.Field()
    field2 = scrapy.Field()

    unique_key = None  # duplicates won't be filtered.


class DemoItem(scrapy.Item):
    # No unique_key is defined. Filtering will be done using `id` field.
    field1 = scrapy.Field()
    field2 = scrapy.Field()
    id = scrapy.Field()


class DemoItem(scrapy.Item):
    field1 = scrapy.Field()
    field2 = scrapy.Field()

    unique_key = "field1"  # Duplicates will be filtered using field1.


class DemoItem(scrapy.Item):
    field1 = scrapy.Field()
    field2 = scrapy.Field()

    unique_key = ("field1", "field2")  # Duplicates will be filtered using both field1 and field2
```
