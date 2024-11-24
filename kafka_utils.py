from subprocess import run


def clear_kafka_topic(broker: str, topic_name: str, retention_time_ms: int = 3600000):
    """
    Clear the messages in a Kafka topic by resetting the retention policy and consumer offset.

    :param broker: Kafka broker address (e.g., 'localhost:9092')
    :param topic_name: Name of the Kafka topic to clear
    :param retention_time_ms: Retention time in milliseconds (default: 1 hour)
    """

    # Step 1: Change retention time to a very low value (to delete old messages)
    print(f"Setting retention time: {retention_time_ms} ms for topic: {topic_name}")
    retention_time_command = f"docker exec -it kafka kafka-configs --alter --topic {topic_name} --add-config retention.ms={retention_time_ms} --bootstrap-server {broker}"
    run(retention_time_command, shell=True)

    print(f"Retention time set for topic {topic_name}.")

    # Step 2: Reset consumer offset (This clears out messages for the consumer)
    reset_offset_command = f"docker exec -it kafka kafka-consumer-groups --bootstrap-server {broker} --group console-consumer --topic {topic_name} --reset-offsets --to-earliest --execute"
    run(reset_offset_command, shell=True)

    print(f"Consumer offsets reset for topic {topic_name}.")
