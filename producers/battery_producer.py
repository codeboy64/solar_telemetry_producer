import json
import time, random, datetime
from utils.helpers import now_iso, battery_update, solar_irradiance, panel_dc_power, inverter_ac_power
from utils.kafka_client import create_producer

producer = create_producer()

def run(site, site_state, telemetry_interval):
    site_id = site["site_id"]
    soc = random.uniform(40, 80)  # initialize once
    battery_capacity_kwh = site["capacity_kw"] * 0.8  # assume battery 80% of site capacity
    interval_hr = telemetry_interval / 3600

    while True:
        # Simulate hour of day
        hour = datetime.datetime.utcnow().hour

        # Solar generation in AC kW
        irr = solar_irradiance(hour)
        dc_power = panel_dc_power(irr) * site["panel_count"]
        ac_power = inverter_ac_power(dc_power)

        # Site consumption (load)
        site_load_kw = site["capacity_kw"] * random.uniform(0.2, 0.6)

        # Update SOC
        soc, mode = battery_update(soc, ac_power, site_load_kw, battery_capacity_kwh, interval_hr)
        site_state[site_id]["battery_soc"] = soc
        site_state[site_id]["inverter_power"] = ac_power  # keep for other producers

        # Prepare message
        msg = {
            "timestamp": now_iso(),
            "site_id": site_id,
            "soc_pct": round(soc, 2),
            "mode": mode,
            "power_kw": round(ac_power - site_load_kw, 2)
        }
        msg_bytes = json.dumps(msg).encode('utf-8')

        producer.send("telemetry.battery", key=site_id.encode(), value=msg_bytes)
        time.sleep(telemetry_interval)
