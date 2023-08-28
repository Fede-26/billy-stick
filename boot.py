# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import machine
machine.freq(240000000)

# import utils.connect_wifi as connect_wifi

# import webrepl
# webrepl.start()

# import main