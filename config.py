import machine
from micropython import const

# BMP180 and LCD display
_scl = const(4)
_sda = const(5)
_freq = const(100000)
i2c = machine.I2C(scl=machine.Pin(_scl), sda=machine.Pin(_sda), freq=_freq)

