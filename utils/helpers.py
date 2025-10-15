import datetime
import math
import random


def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def solar_irradiance(hour):
    """Sinusoidal irradiance (0-1000 W/m²) for 6AM-6PM"""
    if hour < 6 or hour > 18:
        return 0
    return 1000 * math.sin(math.pi * (hour - 6) / 12) * random.uniform(0.9, 1.05)

def panel_dc_power(irradiance, efficiency=0.18, panel_area=1.7):
    """DC power per panel (W)"""
    return irradiance * efficiency * panel_area

def inverter_ac_power(total_dc_power):
    """Convert DC to AC with efficiency"""
    eff = random.uniform(0.97, 0.985)
    return total_dc_power * eff / 1000 # kw

def battery_update(soc, ac_power_kw, site_load_kw, battery_capacity_kwh, interval_hr=1/12):
    """Update battery SOC based on net power"""
    if battery_capacity_kwh <= 0:
        raise ValueError("Battery capacity must be > 0")
    net_kw = ac_power_kw - site_load_kw
    delta_soc = (net_kw / battery_capacity_kwh) * 100 * interval_hr
    soc = max(0, min(100, soc + delta_soc))
    return soc, "charging" if net_kw > 0 else "discharging"
