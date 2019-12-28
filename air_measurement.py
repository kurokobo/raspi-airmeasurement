import json
import os
import time
from os.path import dirname, join

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

import sensor_bme280
import sensor_mhz19b
import sensor_ds18b20

# Load environment variables from .env file
DOTENV_PATH = join(dirname(__file__), ".env")
load_dotenv(DOTENV_PATH)

# Define onstant values
STARTING_BYTE = int.from_bytes(b"\xff", "big")
COMMAND_BYTE = int.from_bytes(b"\x86", "big")


def publish_mqtt(device, cmd, value):
    data = {
        "name": device,
        "cmd": cmd,
        cmd: value,
    }
    print(data)
    client.publish(MQTT_TOPIC, json.dumps(data))


def check_bme280():
    value = sensor_bme280.read()
    publish_mqtt(
        device=os.getenv("DEVICE_NAME"),
        cmd="temperature",
        value=value["temperature"],
    )
    publish_mqtt(
        device=os.getenv("DEVICE_NAME"),
        cmd="humidity",
        value=value["humidity"],
    )
    publish_mqtt(
        device=os.getenv("DEVICE_NAME"),
        cmd="airpressure",
        value=value["airpressure"],
    )


def check_ds18b20():
    value = sensor_ds18b20.read()
    publish_mqtt(
        device=os.getenv("DEVICE_NAME"),
        cmd="temperature",
        value=value["temperature"],
    )


def check_mhz19b():
    value = sensor_mhz19b.read()
    publish_mqtt(
        device=os.getenv("DEVICE_NAME"),
        cmd="co2concentration",
        value=value["co2concentration"],
    )


def main():
    while True:
        check_mhz19b()
        check_bme280()
        # check_ds18b20
        time.sleep(15)


if __name__ == "__main__":
    try:
        MQTT_BROKER = os.getenv("MQTT_BROKER")
        MQTT_TOPIC = os.getenv("MQTT_TOPIC")
        client = mqtt.Client()
        client.connect(MQTT_BROKER)
        client.loop_start()
        main()
    except KeyboardInterrupt:
        client.loop_stop()
