"""Create a topic and produce keyed synthetic order events."""

import json
import socket
from datetime import UTC, datetime

from confluent_kafka import KafkaError, KafkaException, Producer
from confluent_kafka.admin import AdminClient, NewTopic

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "order-events"
EVENTS = [
    {"order_id": 1001, "customer_id": "C101", "status": "created"},
    {"order_id": 1002, "customer_id": "C102", "status": "created"},
    {"order_id": 1003, "customer_id": "C101", "status": "created"},
    {"order_id": 1001, "customer_id": "C101", "status": "shipped"},
]


def ensure_topic() -> None:
    admin = AdminClient({"bootstrap.servers": BOOTSTRAP_SERVERS})
    futures = admin.create_topics(
        [NewTopic(TOPIC, num_partitions=3, replication_factor=1)]
    )
    try:
        futures[TOPIC].result()
        print(f"created topic {TOPIC!r} with 3 partitions")
    except KafkaException as error:
        if error.args[0].code() != KafkaError.TOPIC_ALREADY_EXISTS:
            raise
        print(f"topic {TOPIC!r} already exists")


def delivery_report(error, message) -> None:
    if error is not None:
        print(f"delivery failed: {error}")
        return
    key = message.key().decode("utf-8")
    print(
        f"key={key} -> {message.topic()} partition={message.partition()} "
        f"offset={message.offset()}"
    )


def main() -> None:
    ensure_topic()
    producer = Producer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "client.id": socket.gethostname(),
        }
    )
    for event in EVENTS:
        payload = {
            **event,
            "event_time": datetime.now(UTC).isoformat(),
        }
        producer.produce(
            TOPIC,
            key=event["customer_id"].encode("utf-8"),
            value=json.dumps(payload).encode("utf-8"),
            callback=delivery_report,
        )
        producer.poll(0)

    undelivered = producer.flush(10)
    if undelivered:
        raise RuntimeError(f"{undelivered} event(s) were not delivered")


if __name__ == "__main__":
    main()
