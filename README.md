# ☀️ Solar Telemetry Producer

A solar site telemetry simulator that generates realistic, correlated IoT data streams for solar panels, inverters, batteries, and environmental conditions — and sends them to Kafka topics.

---

## 🚀 Features

- Simulates multiple solar sites with configurable capacity and telemetry intervals
- Produces correlated data between:
    - Solar panels (DC output)
    - Inverters (AC conversion)
    - Batteries (charge/discharge and SOC)
    - Environmental conditions (temperature, irradiance)
- Uses Kafka as a message broker to stream telemetry data
- Topics are auto-created and verified before simulation starts
- Runs as lightweight Docker containers for local testing

---

## 🧠 Realistic Simulation Logic

| Component | Description | Logic Highlights |
|------------|--------------|------------------|
| **Solar irradiance** | Sinusoidal function peaking at midday | 0 W/m² at night, up to ~1000 W/m² at noon |
| **Panel power** | Based on irradiance × panel area × efficiency | Small random variations added |
| **Inverter** | Converts DC → AC | Efficiency ~97–98.5% |
| **Battery** | SOC changes based on net site power (AC – Load) | SOC bounded [0–100%], charge/discharge modes |
| **Environment** | Temperature, irradiance | Reflects diurnal variation |

At night (e.g. before 6 AM or after 6 PM), panel and inverter power drop to 0 — batteries discharge to meet simulated load.

---

## ⚙️ Configuration

`config/sites.yaml` defines your simulated sites:
```yaml
telemetry_interval_sec: 60 # seconds
sites:
  - site_id: SITE-001
    panel_count: 20
    inverter_count: 2
    battery_count: 1
    capacity_kw: 10
  - site_id: SITE-002
    panel_count: 15
    inverter_count: 1
    battery_count: 1
    capacity_kw: 8
```
---
## 📡 Kafka Topics

| Topic                   | Data Type               | Example Payload                                                         |
|-------------------------|------------------------|-------------------------------------------------------------------------|
| `telemetry.panel`       | DC output              | `{ "site_id": "SITE-001", "power_kw": 82.3 }`                           |
| `telemetry.inverter`    | AC power               | `{ "site_id": "SITE-001", "ac_power_kw": 79.9, "efficiency_pct": 98.1 }`|
| `telemetry.battery`     | Battery state          | `{ "soc_pct": 73.5, "mode": "charging" }`                               |
| `telemetry.environment` | Temperature, irradiance| `{ "temp_c": 27.4, "irradiance": 812 }`                                 |
---
## 🐳 Running the Simulator (Local / Docker)
Build & start Kafka + simulator with Docker Compose

`docker-compose up -d`

You should see:
- ✅ Connected to Kafka broker
- 🚀 Correlated telemetry producers running...

---
## 📊 Viewing Messages

Consume messages from Kafka:

```
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic telemetry.battery \
  --from-beginning
```
---
## 🧪 Example Output
```
{"timestamp": "2025-10-15T05:12:47.314Z", "site_id": "SITE-002", "soc_pct": 73.4, "mode": "charging", "power_kw": 4.18}
{"timestamp": "2025-10-15T05:12:47.339Z", "site_id": "SITE-001", "soc_pct": 65.9, "mode": "charging", "power_kw": 5.02}
```
---

## ⚙️ Project Structure
```
solar_telemetry_producer/
├── config/
│ └── sites.yaml
├── producers/
│ ├── panel_producer.py
│ ├── inverter_producer.py
│ ├── battery_producer.py
│ └── environment_producer.py
├── utils/
│ ├── create_topics.py
│ ├── kafka_client.py
│ └── helpers.py
├── docker-compose.yml
├── main.py
└── README.md
```
---
## 🧠 Future Enhancements
- Simulate cloud cover / weather variations
- Introduce fault injection (e.g., inverter offline)
- Add Prometheus metrics for monitoring
- Stream to external data sinks (e.g., TimescaleDB)
---