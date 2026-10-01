"""Consume order events while exposing group, partition, offset, and commits."""

import argparse
import json

from confluent_kafka import Consumer, KafkaException

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "order-events"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", default="order-lab")
    parser.add_argument(
        "--from-beginning",
        action="store_true",
        help="Use earliest only when the group has no valid committed offset.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Synchronously commit each successfully printed message.",
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=0,
        help="Stop after N messages; zero waits until Ctrl+C.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    consumer = Consumer(
        {
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "group.id": args.group,
            "enable.auto.commit": False,
            "auto.offset.reset": ("earliest" if args.from_beginning else "latest"),
        }
    )
    consumer.subscribe([TOPIC])
    count = 0
    print(
        f"consumer group={args.group!r}; commit={args.commit}; "
        "waiting for records (Ctrl+C to stop)"
    )
    try:
        while not args.max_messages or count < args.max_messages:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                raise KafkaException(message.error())

            event = json.loads(message.value().decode("utf-8"))
            key = message.key().decode("utf-8") if message.key() else None
            print(
                f"key={key} partition={message.partition()} "
                f"offset={message.offset()} value={event}"
            )
            count += 1
            if args.commit:
                consumer.commit(message=message, asynchronous=False)
                print(f"  committed next offset {message.offset() + 1}")
    except KeyboardInterrupt:
        print("\nstopping")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
