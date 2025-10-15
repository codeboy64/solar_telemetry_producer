# Solar Telemetry Kafka Simulator

Simulates solar panel, inverter, battery, and environmental telemetry
and sends it to Kafka topics for testing and monitoring pipelines.

## Summary
- main.py → orchestrates threads for all sites & device types.
- producers/ → modular code for each device type (panel, inverter, battery, environment).
- config/sites.yaml → lets you scale dynamically by defining sites & device counts.

## Kafka Topics
- telemetry.panel
- telemetry.inverter
- telemetry.battery
- telemetry.environment

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Start Kafka locally or connect to your cluster
3. Run: `python main.py`
