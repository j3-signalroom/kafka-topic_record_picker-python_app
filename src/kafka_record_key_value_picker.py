import logging
from typing import Dict
from confluent_kafka import KafkaConsumer, TopicPartition


__copyright__  = "Copyright (c) 2025 Jeffrey Jonathan Jennings"
__credits__    = ["Jeffrey Jonathan Jennings (J3)"]
__maintainer__ = "Jeffrey Jonathan Jennings (J3)"
__email__      = "j3@thej3.com"
__status__     = "dev"


class KafkaRecordKeyValuePicker:
    """This class picks a specific key/value record from a Kafka topic partition at a given offset."""

    def __init__(self, properties: Dict, polling_in_ms: int, topic_name: str):
        """Initialize the Kafka consumer with the given properties, polling duration, and topic name.

        Arg(s):
            properties (dict):    Dictionary of Kafka consumer configuration properties.
            polling_in_ms (int):  Polling duration in milliseconds.
            topic_name (str):     Name of the Kafka topic.
        """
        self.topic_name = topic_name
        self.polling_in_ms = polling_in_ms
        # Assuming properties is a dict with valid KafkaConsumer parameters, such as bootstrap_servers, group_id, etc.
        self.consumer = KafkaConsumer(**properties)
        self.logger = logging.getLogger(self.__class__.__name__)

    def pick_key_value_record(self, offset: int, partition: int):
        """Read a specific key/value record from the Kafka cluster at the specified offset within a topic partition.

        Arg(s):
            offset (int):       The offset to seek to.
            partition (int):    The partition number.
        """
        # Create a TopicPartition instance for the given topic and partition.
        topic_partition = TopicPartition(self.topic_name, partition)
        # Assign the consumer to this partition.
        self.consumer.assign([topic_partition])
        # Seek to the specified offset.
        self.consumer.seek(topic_partition, offset)

        self.logger.info("Picking key/value record in partition %s at offset %s.", partition, offset)

        while True:
            try:
                # Poll returns a dictionary mapping TopicPartition to a list of records.
                records = self.consumer.poll(timeout_ms=self.polling_in_ms)
                total_records = sum(len(record_list) for record_list in records.values())
                self.logger.info("%s number of records to consume.", total_records)

                # Iterate through the records and return the first one found.
                for tp, record_list in records.items():
                    for record in record_list:
                        self.logger.info("Key: %s\nValue: %s", record.key, record.value)
                        return record

            except Exception as e:
                self.logger.error("Exception occurred: %s", e)
                return None

    def close(self):
        """Close the Kafka consumer."""
        self.consumer.close()

    def __enter__(self):
        """Allow use in 'with' statements."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
