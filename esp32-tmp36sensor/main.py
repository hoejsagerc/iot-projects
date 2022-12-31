from machine import Pin, ADC
import time
import ConnectToWifi
import urequests
import usocket
import json
import gc

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
    headers = {"Content-Type": "application/json"}
    try:
        response = urequests.post(url, data=json_obj, headers=headers)
        print(response.status_code)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    gc.enable()
    ConnectToWifi.connect()
    
    sensors = {
        "sensor_1": 36,
        "sensor_2": 35,
        "sensor_3": 34,
        "sensor_4": 33,
        "sensor_5": 32
    }

    access_token = ""
    
    while True:
        response_obj = {}
        for key in sensors:
            response_obj[key] = collect_data_on_pin(sensors[key])
         
        print(response_obj)
        post_data(data=response_obj, url=f"https://iot.scriptingchris.tech/api/v1/{access_token}/telemetry")
        time.sleep(15)
        gc.collect()
    