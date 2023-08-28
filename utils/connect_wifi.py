import time
import network
from data.networks import NETWORKS

wlan = network.WLAN(network.STA_IF)
if not wlan.active() or not wlan.isconnected():
    wlan.active(True)
    print("Trying to connect to wifi...")
    for net in NETWORKS:
        print("Connecting to "+net["ssid"])
        wlan.connect(net["ssid"], net["psw"])
        for i in range(10):
            print(".", end="")
            if wlan.isconnected():
                print("\nCONNECTED!")
                break
            time.sleep(1)
        if wlan.isconnected():
            break