import json
import time, random
from kafka import KafkaProducer
from utils.helpers import now_iso, battery_update
from utils.kafka_client import create_producer

producer = create_producer()

def run(site, site_state):
    site_id = site["site_id"]
    soc = random.uniform(40, 80)
    battery_capacity_kwh = site["capacity_kw"] * 0.8  # assume battery 80% of site capacity

    while True:
        ac_power = site_state[site_id]["inverter_power"]
        site_load_kw = site["capacity_kw"] * random.uniform(0.2, 0.6)
        soc, mode = battery_update(soc, ac_power, site_load_kw, battery_capacity_kwh)
        site_state[site_id]["battery_soc"] = soc

        msg = {
            "timestamp": now_iso(),
            "site_id": site_id,
            "soc_pct": round(soc,2),
            "mode": mode,
            "power_kw": round(ac_power - site_load_kw, 2)
        }
        msg_bytes = json.dumps(msg).encode('utf-8')

        producer.send("telemetry.battery", key=site_id.encode(), value=msg_bytes)
        time.sleep(10)
