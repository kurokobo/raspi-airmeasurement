import json
import os
import time
from os.path import dirname, join
from glob import glob

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables from .env file
DOTENV_PATH = join(dirname(__file__), ".env")
load_dotenv(DOTENV_PATH)



def publish_mqtt(device, cmd, value):
    data = {
        "name": device,
        "cmd": cmd,
        cmd: value,
    }
    print(data)
    client.publish(MQTT_TOPIC, json.dumps(data))
    

def check_temperature():
    valuefile = open(glob("/sys/bus/w1/devices/28-*")[0] + "/w1_slave")
    text = valuefile.read()
    valuefile.close()

    line = text.split("\n")[1]
    rawdata = line.split(" ")[9]
    temperature = float(rawdata[2:])
    temperature = temperature / 1000

    publish_mqtt(device=os.getenv("DEVICE_NAME"), cmd="temperature", value=temperature)


def main():
    while True:
        check_temperature()
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

