import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, NodeNotReadyError


def ensure_topics():
    while True:
        try:
            admin = KafkaAdminClient(bootstrap_servers="kafka:9092")
            topics = admin.list_topics()
            for t in ["telemetry.panel", "telemetry.inverter", "telemetry.battery", "telemetry.environment"]:
                if t not in topics:
                    admin.create_topics([NewTopic(name=t, num_partitions=1, replication_factor=1)])
            print("✅ Topics ensured")
            return
        except KafkaError as e:
            print(f"⚠️ Kafka not ready, retrying in 5s... ({e})")
            time.sleep(5)

def wait_for_kafka(bootstrap_servers="kafka:9092", timeout=120):
    start_time = time.time()
    while True:
        try:
            admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            # Try listing topics to ensure controller is ready
            admin.list_topics()
            print("✅ Kafka is ready")
            return
        except (NodeNotReadyError, KafkaError) as e:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Kafka did not become ready in {timeout}s: {e}")
            print("⚠️ Kafka not ready, retrying in 5s...")
            time.sleep(5)