from confluent_kafka import KafkaConsumer, TopicPartition


__copyright__  = "Copyright (c) 2025 Jeffrey Jonathan Jennings"
__credits__    = ["Jeffrey Jonathan Jennings (J3)"]
__maintainer__ = "Jeffrey Jonathan Jennings (J3)"
__email__      = "j3@thej3.com"
__status__     = "dev"


class KafkaRecordValuePicker:
    """
    A Python version of the KafkaRecordValuePicker.
    
    This class creates a KafkaConsumer based on given properties and provides methods
    to pick a value record, pick a value record schema (by converting the record's value to string),
    and pick the full record from a specific topic partition and offset.
    """
    def __init__(self, properties, polling_in_ms, topic_name):
        """
        Initializes the KafkaRecordValuePicker.
        
        :param properties: A dictionary of configuration properties for the KafkaConsumer.
        :param polling_in_ms: The polling duration in milliseconds.
        :param topic_name: The name of the Kafka topic.
        """
        self.topic_name = topic_name
        self.polling_in_ms = polling_in_ms
        self.kafka_consumer = KafkaConsumer(**properties)
    
    def pick_value_record(self, offset, partition):
        """
        Polls until a non-null record value is found at the given offset and partition,
        and then returns that value.
        
        :param offset: The offset from which to start polling.
        :param partition: The partition number.
        :return: The value of the Kafka record.
        """
        tp = TopicPartition(self.topic_name, partition)
        self.kafka_consumer.assign([tp])
        self.kafka_consumer.seek(tp, offset)
        
        while True:
            records = self.kafka_consumer.poll(timeout_ms=self.polling_in_ms)
            for topic_partition, messages in records.items():
                for message in messages:
                    if message.value is not None:
                        return message.value
    
    def pick_value_record_schema(self, offset, partition):
        """
        Polls until a non-null record value is found at the given offset and partition,
        and then returns the string representation of that value.
        
        :param offset: The offset from which to start polling.
        :param partition: The partition number.
        :return: The string representation of the Kafka record value.
        """
        tp = TopicPartition(self.topic_name, partition)
        self.kafka_consumer.assign([tp])
        self.kafka_consumer.seek(tp, offset)
        
        while True:
            records = self.kafka_consumer.poll(timeout_ms=self.polling_in_ms)
            for topic_partition, messages in records.items():
                for message in messages:
                    if message.value is not None:
                        return str(message.value)
    
    def pick_record(self, offset, partition):
        """
        Polls until a non-null record is found at the given offset and partition,
        and then returns the complete record.
        
        :param offset: The offset from which to start polling.
        :param partition: The partition number.
        :return: The Kafka record (message).
        """
        tp = TopicPartition(self.topic_name, partition)
        self.kafka_consumer.assign([tp])
        self.kafka_consumer.seek(tp, offset)
        
        while True:
            records = self.kafka_consumer.poll(timeout_ms=self.polling_in_ms)
            for topic_partition, messages in records.items():
                for message in messages:
                    if message.value is not None:
                        return message
    
    def close(self):
        """
        Closes the Kafka consumer.
        """
        self.kafka_consumer.close()
