from machine import Pin, ADC
import ConnectToWifi
import time
import urequests
import json
import gc


class TempObject:
    def __init__(self, name: str, pin: int):
        self.name = name
        self.pin = pin
        self.temp_list = []
        self.count = 0

    def read_database(self):
        with open("data.json", "r") as jsonfile:
            data = json.load(jsonfile)
        self.temp_list = data[self.name]["temp_list"]
        self.count = data[self.name]["count"]

    def write_database(self):
        with open("data.json", "r") as jsonfile:
            data = json.load(jsonfile)
        data[self.name]["temp_list"] = self.temp_list
        data[self.name]["count"] = self.count
        with open("data.json", "w") as jsonfile:
            json.dump(data, jsonfile)

    def first_time_initialize(self):
        self.read_database()
        temp = self.read_data()
        for i in range(len(self.temp_list)):
            self.temp_list[i] = temp
        self.write_database()

    def check_count(self):
        if self.count == 20:
            self.count = 0

    def read_data(self):
        try:
            adc = ADC(Pin(self.pin))
            adc.atten(ADC.ATTN_11DB)
            temp_read = adc.read()
            temp_volt = temp_read * 3.3 / 4096
            temp = (temp_volt - 0.33) * 100.0
        except Exception as e:
            print(f"failed reading data on ping: {self.pin} - {e}")
            temp = 0.0
        return temp

    def blink_led(self):
        try:
            led = Pin(2, Pin.OUT)
            led.value(1)
            time.sleep(0.2)
            led.value(0)
        except Exception as e:
            print(f"Failed executing LED - {e}")

    def collect_data(self):
        self.read_database()
        self.check_count()
        self.temp_list[self.count] = self.read_data()
        self.count += 1
        self.write_database()
        self.blink_led()
        avg_temp = sum(self.temp_list) / len(self.temp_list)
        return avg_temp

    def post_data(self, data: dict, url: str):
        json_obj = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        try:
            response = urequests.post(url, data=json_obj, headers=headers)
            return response.status_code
        except Exception as e:
            print(e)


if __name__ == "__main__":
    ssid = ""  # <-- Enter your wifi ssid here
    password = ""  # <-- Enter your wifi password here
    iot_device_url = "https://iot.scriptingchris.tech/api/v1/7SmWXFwT4aPv5qs67lQm/telemetry"  # <-- Enter your iot device url here

    ConnectToWifi.connect(ssid=ssid, password=password)

    s1 = TempObject(name="sensor_1", pin=35)  # <-- Map the pin to the sensor here and forach sensor below
    s1.first_time_initialize()
    s2 = TempObject(name="sensor_2", pin=36)
    s2.first_time_initialize()
    s3 = TempObject(name="sensor_3", pin=34)
    s3.first_time_initialize()
    s4 = TempObject(name="sensor_4", pin=33)
    s4.first_time_initialize()
    s5 = TempObject(name="sensor_5", pin=32)
    s5.first_time_initialize()

    sensors = {
        s1.name: s1,
        s2.name: s2,
        s3.name: s3,
        s4.name: s4,
        s5.name: s5
    }

    gc.enable()
    while True:
        gc.enable()
        data_obj = {}
        for key in sensors:
            data_obj[key] = sensors[key].collect_data()
            print(f"sensor: {key} - avg temp: {data_obj[key]} - count: {sensors[key].count}")
            print(sensors[key].temp_list)
        sensors["sensor_1"].post_data(data=data_obj, url=iot_device_url)
        time.sleep(1)
        gc.collect()
