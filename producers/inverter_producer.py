import json
import time
from kafka import KafkaProducer
from utils.helpers import now_iso, inverter_ac_power
from utils.kafka_client import create_producer

producer = create_producer()

def run(site, site_state):
    site_id = site["site_id"]
    while True:
        dc_power = site_state[site_id]["panel_power"]
        ac_power = inverter_ac_power(dc_power)
        site_state[site_id]["inverter_power"] = ac_power

        msg = {
            "timestamp": now_iso(),
            "site_id": site_id,
            "ac_power_kw": round(ac_power, 2),
            "efficiency_pct": round((ac_power / (dc_power / 1000) * 100), 2) if dc_power > 0 else 0
        }
        msg_bytes = json.dumps(msg).encode('utf-8')

        producer.send("telemetry.inverter", key=site_id.encode(), value=msg_bytes)
        time.sleep(5)
