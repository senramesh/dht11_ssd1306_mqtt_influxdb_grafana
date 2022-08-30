## OLED SCK --> GPIO 22
## OLED SDA --> GPIO 21
## OLED VDD --> Bat
## OLED GND --> GND

## DHT11 S --> GPIO 14
## DHT11 S --> GND
## DHT11 S --> 3V

import utime
import ujson
import machine
import ssd1306
from ntptime import settime
import dht
from umqtt_simple import MQTTClient
import ubinascii

# Set time from pool.ntp.org time servers
settime()

# Initialize the DHT11
sensor = dht.DHT11(machine.Pin(14))

# Initialize the ssd1306 OLED
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

# Initialize the MQTT related variable
mqtt_server = "MQTT SERVER IP"
mqtt_port = "1883"
mqtt_user = "admin"
mqtt_password = "YOUR MQTT PASSWORD"
esp32_uid = ubinascii.hexlify(machine.unique_id())

# Function to publish the MQTT messages to Mosquitto MQTT
def publish(mqtt_topic, mqtt_message):
    c = MQTTClient(esp32_uid, mqtt_server, mqtt_port, mqtt_user, mqtt_password)
    c.connect()
    c.publish(mqtt_topic, mqtt_message)
    c.disconnect()

# Main loop
while True:
    # Initialize
    oled.fill(0)
    errmessage = ""
    
    try:
        sensor.measure()
         HomeTemperature = sensor.temperature()
         HomeHumidity = sensor.humidity()
    except OSError as e:
        errmessage = "ERR Sensor"
    
    # Feed the DXB Home Temperature data to OLED
    oled.text('Temperature :' + str(HomeTemperature), 1, 1, 1)
    oled.text('Humidity    :' + str(HomeHumidity), 1, 2, 1)

    # Send to MQTT the DXB Home Temperature data
    try:
        publish("ESP32/ _dht11_sensor1", "Temperature:" + str(HomeTemperature) + ", Humidity:" + str(HomeHumidity))
    except:
        errmessage = "ERR MQTT"
    
    # If any error found show in OLED
    if not errmessage:
        oled.text(errmessage, 1, 24, 1)

    #oled.text('Temp2', 1, 24, 1)

    # Send the feeds to the OLED
    oled.show()
    
    # Sleep for a while
    utime.sleep(30)

