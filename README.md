# scrapy-item-pipelines

Various scrapy item pipelines

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
