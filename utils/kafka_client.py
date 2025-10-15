# utils/kafka_client.py
import time
from kafka import KafkaProducer, errors

def create_producer(max_retries=12, delay=5):
    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=["kafka:9092"],
                value_serializer=lambda v: v,
                api_version_auto_timeout_ms=10000,
            )
            print("✅ Connected to Kafka broker")
            return producer
        except errors.NoBrokersAvailable:
            print(f"⚠️  Kafka not yet available (attempt {attempt+1}), retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("Kafka broker not reachable after several attempts")
