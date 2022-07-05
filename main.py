from lcd import lcd
from wifimngr import wifi

wifi.connect()
lcd.putstr("Hello World")
