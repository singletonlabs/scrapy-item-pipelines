from functools import partial

from scrapy.exceptions import NotConfigured
from scrapy.utils.serialize import ScrapyJSONEncoder
from itemadapter import ItemAdapter

from confluent_kafka import Producer


class PushToKafkaPipeline:
    """Scrapy Item Pipeline to push items to Apache Kafka"""

    @classmethod
    def from_settings(cls, settings):
        """
        Args:
            settings: Scrapy settings instance."""

        project_settings = settings.get("SL_SCRAPY_ITEM_PIPELINES_SETTINGS", {})
        kafka_hosts = project_settings.get("push_to_kafka_hosts", "localhost:9092")
        kafka_default_topic = project_settings.get("push_to_kafka_default_topic")
        item_encoder = project_settings.get("push_to_kafka_item_encoder")
        return cls(kafka_hosts, kafka_default_topic, item_encoder)

    def __init__(self, kafka_hosts, kafka_default_topic, item_encoder=None):
        """
        Args:
            kafka_hosts (str): Kafka hosts. Separated by commas.
            kafka_default_topic (str): Defualt kafka topic to use if item has
                                       no topic defined.
            item_encoder (func): Encoder to use. If None scrapy json encoder
                                 is used."""

        self.kafka_hosts = kafka_hosts
        self.default_topic = kafka_default_topic
        self.item_encoder = item_encoder() if item_encoder else ScrapyJSONEncoder()

    def kafka_produce_ack(self, spider, err, msg):
        """Handle kafka product acknowledge messages.
        Args:
            spider (scrapy.Spider)
            err
            msg"""

        if err is not None:
            spider.crawler.stats.inc_value("kafka_pipeline_push_error_count")
            spider.crawler.stats.inc_value(
                f"kafka_pipeline_error_reason_{err.str()}_push_error_count"
            )
            spider.crawler.stats.inc_value(
                f"kafka_pipeline_topic_{msg.topic()}_push_error_count"
            )

    def process_item(self, item, spider):
        """Push item to kafka.
        Args:
            item (scrapy.Item)
            spider (scrapy.Spider)"""

        try:
            topic = item.kafka_topic
        except AttributeError:
            topic = self.default_topic

        if topic is None:
            err_msg = """
                SL_SCRAPY_ITEM_PIPELINES_SETTINGS.push_to_kafka_default_topic
                or item.kafka_topic should be defined
            """
            raise NotConfigured(err_msg)

        kafka_ack = partial(self.kafka_produce_ack, spider)
        item_adapted = ItemAdapter(item)
        try:
            data_key = item_adapted.get(item_adapted.kafka_data_key)
        except AttributeError:
            data_key = None

        data = self.item_encoder.encode(item)

        # trigger any previous acknowledges
        self.kafka_producer.poll(1)
        self.kafka_producer.produce(topic, key=data_key, value=data, callback=kafka_ack)
        return item

    def open_spider(self, spider):
        self.kafka_producer = Producer({"bootstrap.servers": self.kafka_hosts})

    def close_spider(self, spider):
        self.kafka_producer.flush(5)
