# Kafka producer/consumer mini-lab

This local, single-broker lab demonstrates record keys, partitions, consumer groups, offsets, commits, and replay. Docker runs Kafka in KRaft mode; Python scripts use synthetic order events.

## Run

Prerequisites: Docker Compose and Python 3.10+.

```powershell
docker compose up -d
uv run --with-requirements requirements.txt python producer.py
uv run --with-requirements requirements.txt python consumer.py --group fulfillment-a --from-beginning --commit --max-messages 4
uv run --with-requirements requirements.txt python consumer.py --group fulfillment-a --from-beginning
uv run --with-requirements requirements.txt python consumer.py --group audit-replay-1 --from-beginning --max-messages 4
docker compose down -v
```

The producer creates `order-events` with three partitions when absent and uses `customer_id` as the key. Kafka's partitioner normally sends the same serialized key to the same partition, preserving order only within that partition. Delivery callbacks print the resulting topic/partition/offset.

The first committed `fulfillment-a` run advances that group's offsets. The second run should wait without replaying old records because `auto.offset.reset` only applies where that group has no valid committed offset. A new `audit-replay-1` group reads independently from the beginning. Stop a waiting consumer with Ctrl+C.

For an explicit same-group rewind, stop its consumers, then run:

```powershell
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group fulfillment-a --topic order-events --reset-offsets --to-earliest --execute
uv run --with-requirements requirements.txt python consumer.py --group fulfillment-a
```

## Concepts to observe

- A key influences partition selection; it does not globally order the topic.
- Consumers sharing one group divide partitions, so one partition is assigned to at most one active consumer in that group.
- Different groups maintain independent committed offsets.
- An offset identifies a record's position within one topic-partition, not across the whole topic.
- This consumer disables auto-commit. `--commit` commits each successfully printed message, favoring clarity over throughput.

Try two terminals with the same group, then a third consumer: with three partitions, assignments rebalance across up to three active group members. Run the producer again while they are active.

## Honest boundaries

This is one ephemeral plaintext broker, not a production cluster. It omits replication, broker failure, TLS/SASL, schema registry, ACLs, idempotent/transactional processing, dead-letter handling, monitoring, capacity planning, and rolling operations. Printing before a synchronous commit illustrates mechanics but does not make an external side effect exactly-once. Docker image tags should be reviewed and updated like any dependency.

## Interview talking points

- Explain key-based affinity and partition-level ordering.
- Contrast consumer position with committed group offset and explain when `auto.offset.reset` matters.
- Describe rebalances and why partition count bounds active consumers in one group.
- Discuss at-least-once processing: perform idempotent work, then commit; failures between those actions can replay.
- State clearly that the exercise demonstrates Kafka semantics, not operating a resilient production cluster.
