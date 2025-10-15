import threading, yaml
import time

from producers import panel_producer, inverter_producer, battery_producer, environment_producer
from utils.create_topics import ensure_topics, wait_for_kafka

# Load config
with open("config/sites.yaml") as f:
    config = yaml.safe_load(f)
sites = config["sites"]

# Shared state for correlation
site_state = {site["site_id"]: {"battery_soc":50.0, "panel_power":0.0, "inverter_power":0.0} for site in sites}

wait_for_kafka()
ensure_topics()

# Start producers
for site in sites:
    threading.Thread(target=panel_producer.run, args=(site, site_state), daemon=True).start()
    threading.Thread(target=inverter_producer.run, args=(site, site_state), daemon=True).start()
    threading.Thread(target=battery_producer.run, args=(site, site_state), daemon=True).start()
    threading.Thread(target=environment_producer.run, args=(site,), daemon=True).start()

print("🚀 Correlated telemetry producers running...")
while True:
    time.sleep(1)
