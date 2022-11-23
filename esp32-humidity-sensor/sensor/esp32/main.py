import ConnectWifi
import esp32
import time


INTERVAL = 1

def collect_data():
    while True:
        tf = esp32.raw_temperature()
        tc = (tf-32.0)/1.8
        print(tc)
        time.sleep(INTERVAL)

        
        
if __name__=="__main__":
    ConnectWifi.connect()
    collect_data()