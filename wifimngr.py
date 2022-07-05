# import socket
import time
import network

from lcd import lcd


class WiFi:
    def __init__(self):
        # self.ap_ssid = "ESP8266WifiManager"
        # self.ap_password = "#rajibul"
        # self.ap_authmode = 3  # WPA2-PSK
        self.NETWORK_PROFILES = "wifi.dat"

        # self.server_socket = None
        # self.wlan_ap = network.WLAN(network.AP_IF)
        self.wlan_sta = network.WLAN(network.STA_IF)
        # self.connected = self.wlan_sta.isconnected()

        self.authmode = {0: "open", 1: "WEP", 2: "WPA-PSK",
                         3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}

    def connect(self):
        lcd.putstr("Connecting to Wifi", True)
        if self.wlan_sta.isconnected():
            lcd.putstr("Wifi Connected\n", True)
            return True

        connected = False
        profiles = self.read_profiles()
        self.wlan_sta.active(True)
        networks = self.wlan_sta.scan()

        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            print(f"ssid: {ssid} chan: {channel} rssi: {rssi} authmode: {self.authmode.get(authmode, '?')}")
            if authmode > 0:
                if ssid in profiles:
                    connected = self._connect(ssid=ssid, password=profiles[ssid])
            else:
                connected = self._connect(ssid, None)
            if connected is not False:
                break
        if connected:
            lcd.putstr("Wifi Connected\n", True)
        else:
            lcd.putstr("Wifi not connected\n", True)
        return connected

    def read_profiles(self):
        profiles = {}
        with open(self.NETWORK_PROFILES) as f:
            for line in f:
                ssid, password = line.strip("\n").split(";")
                profiles[ssid] = password
        return profiles

    def _connect(self, ssid, password):
        self.wlan_sta.active(True)
        if self.wlan_sta.isconnected():
            return None

        print(f'Trying to connect...\nSSID:{ssid}')
        print(f'Password:{password[:3]}{"*" * (len(password) - 3)}')
        connected = False
        self.wlan_sta.connect(ssid, password)
        for retry in range(100):
            connected = self.wlan_sta.isconnected()
            if connected:
                break
            time.sleep(0.1)
            print('.', end='')
        if connected:
            print('\nConnected. Network config: ', self.wlan_sta.ifconfig())
        else:
            print('\nFailed. Not Connected to: ' + ssid)
        return connected
wifi = WiFi()
