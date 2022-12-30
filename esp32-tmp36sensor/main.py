from machine import Pin, ADC
import time
import ConnectToWifi
import urequests
import json

#response = urequests.post("http://192.168.1.232/temps/", data=data)

def collect_data_on_pin(pin: int):
    try:
        adc = ADC(Pin(pin))
        adc.atten(ADC.ATTN_11DB)
        temp_read = adc.read()
        temp_volt = temp_read * 3.3 / 4096
        temp = (temp_volt - 0.33) * 100.0
    except:
        temp = 0.0
    return temp


def post_data(data, url):
    json_obj = json.dumps(data)
    try:
        response = urequest.post(url, data=json_obj)
        print(response.status_code)
    except
        print("Failed posting data to the api")

        

if __name__=="__main__":
    ConnectToWifi.connect()
    
    sensors = {
        "sensor_1": 36,
        "sensor_2": 35,
        "sensor_3": 34,
        "sensor_4": 33,
        "sensor_5": 32
    }
    
    while True:
        response_obj = {}
        for key in sensors:
            response_obj[key] = collect_data_on_pin(sensors[key])
         
        print(response_obj)
        post_data(data=response_obj, url="http://192.168.1.232/items/")
        time.sleep(15)
    
        
    