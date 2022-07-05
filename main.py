import machine
from micropython import const
from i2c_lcd import I2cLcd
from config import i2c


def wait_for_lcd():
    print("Configuring LCD")
    led = machine.Pin(2, machine.Pin.OUT)
    led.on()
    while 1:
        i2c_devices = i2c.scan()
        print(f"Found I2C devices at: {i2c_devices}")
        if 0x27 in i2c_devices:
            break
        led.value(not led.value())
        time.sleep_ms(200)

    if 0x27 in i2c_devices:
        print("Found LCD Display")
    if 0x77 in i2c_devices:
        print("Found BMP180 Sensor")
    return I2cLcd(i2c, 0x27, 2, 16)


lcd = wait_for_lcd()
lcd.putstr("Hello World")
