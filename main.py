from lcd import lcd
from wifimngr import wifi
from local_server import server

wifi.connect()
lcd.putstr("Hello World\n")
lcd.putstr(wifi.wlan_sta.ifconfig()[0])
gc.collect()
server.run()
