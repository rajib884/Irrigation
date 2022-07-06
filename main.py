import ESPWebServer
import network
import machine
import json
import time
from lcd import lcd
from wifimngr import wifi

wifi.connect()
lcd.putstr(wifi.wlan_sta.ifconfig()[0])

moisture_sensor = machine.ADC(0)

GPIO_NUM = 2
motor = machine.Pin(GPIO_NUM, machine.Pin.OUT)
motor.on()  # Turn LED off (it use sinking input)

data = {
    "status": "Dry",
    "switch": "On",
    "value": 0,
    "values": [0] * 100, # ten zeros in this list
}


# Update information
def updateInfo(socket):
    global data
    data["status"] = "Wet" if motor.value() else "Dry"
    data["switch"] = "On" if motor.value() else "Off"
    # data["value"] = moisture_sensor.read()
    ESPWebServer.ok(
        socket,
        "200",
        "application/json",
        json.dumps(data)
    )


def handleSwitch(socket, args):
    motor.value(not motor.value())  # Switch back and forth
    updateInfo(socket)


def update(socket, args):
    updateInfo(socket)


ESPWebServer.begin()  # use default 80 port
ESPWebServer.onPath("/switch", handleSwitch)
ESPWebServer.onPath("/update", update)
ESPWebServer.setDocPath("server")
ESPWebServer.setMaxContentLength(1024)

last_reading = time.time()

try:
    while True:
        # Let server process requests
        ESPWebServer.handleClient()
        current_time = time.time()
        if current_time != last_reading:
            last_reading = current_time
            data["value"] = moisture_sensor.read()
            data["values"].pop(0)
            data["values"].append(data["value"])
except:
    ESPWebServer.close()
