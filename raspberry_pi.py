import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# MQTT Configuration
BROKER = "your_mqtt_broker_ip"
PORT = 1883
TOPIC_SUBSCRIBE = "home/control"
TOPIC_PUBLISH = "home/sensor_data"
CLIENT_ID = "RaspberryPi_Client"

# Sensor and GPIO Setup
DHT_SENSOR = Adafruit_DHT.DHT11  # Using a DHT11 sensor
DHT_PIN = 4  # GPIO pin for sensor
RELAY_PIN = 17  # GPIO pin for appliance control

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Callback function when connected to broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(TOPIC_SUBSCRIBE)

# Callback function when message received
def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Received command: {command}")
    
    if command == "ON":
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    elif command == "OFF":
        GPIO.output(RELAY_PIN, GPIO.LOW)

# MQTT Client Setup
client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

# Main loop to read sensor and send data
try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            sensor_data = f"Temp: {temperature:.1f}C, Humidity: {humidity:.1f}%"
            client.publish(TOPIC_PUBLISH, sensor_data)
            print(f"Published: {sensor_data}")
        else:
            print("Sensor failure. Check wiring.")
        
        time.sleep(5)  # Send data every 5 seconds

except KeyboardInterrupt:
    print("Stopping script.")
    GPIO.cleanup()
    client.disconnect()
