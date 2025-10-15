import json
import time, random, datetime
from kafka import KafkaProducer
from utils.helpers import now_iso, solar_irradiance, panel_dc_power
from utils.kafka_client import create_producer

producer = create_producer()

def run(site, site_state):
    site_id = site["site_id"]
    panel_count = site["panel_count"]
    while True:
        hour = datetime.datetime.utcnow().hour + datetime.datetime.utcnow().minute/60
        irr = solar_irradiance(hour)
        dc_per_panel = panel_dc_power(irr)
        total_dc = dc_per_panel * panel_count

        # Update shared state
        site_state[site_id]["panel_power"] = total_dc

        msg = {
            "timestamp": now_iso(),
            "site_id": site_id,
            "avg_panel_power_w": round(dc_per_panel, 2),
            "total_dc_power_w": round(total_dc, 2),
            "irradiance_wm2": round(irr, 2)
        }
        msg_bytes = json.dumps(msg).encode('utf-8')

        producer.send("telemetry.panel", key=site_id.encode(), value=msg_bytes)
        time.sleep(2)
