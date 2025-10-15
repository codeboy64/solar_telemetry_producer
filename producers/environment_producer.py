import json
import random, time
from kafka import KafkaProducer
from utils.helpers import now_iso
from utils.kafka_client import create_producer

producer = create_producer()

def run(site):
    site_id = site["site_id"]
    while True:
        msg = {
            "timestamp": now_iso(),
            "site_id": site_id,
            "sensor_id": f"{site_id}-SEN01",
            "ambient_temp_c": random.uniform(20, 35),
            "wind_speed_ms": random.uniform(0, 10),
            "humidity_pct": random.uniform(20, 80)
        }
        msg_bytes = json.dumps(msg).encode('utf-8')

        producer.send("telemetry.environment", key=site_id.encode(), value=msg_bytes)
        time.sleep(15)
