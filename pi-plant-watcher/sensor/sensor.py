import os
import glob
import time
import json
import logging
from datetime import datetime
from tokenize import Double
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse



logging.basicConfig(level=logging.ERROR)


def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def timestamp():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = round(float(temp_string) / 1000.0, 2)
        #data = '{{"temperature": {temperature},"logtime": {logtime}}}'
        #data = '''{{"temperature": {temperature}}}'''
        #message = data.format(temperature=temp_c, logtime=timestamp())
        #message = data.format(temperature=temp_c)
        message = json.dumps({
            "temperature": temp_c,
            "logtime": timestamp()
        })
        return message


def create_client():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Define a method request handler
    def method_request_handler(method_request):
        if method_request.name == "SetTelemetryInterval":
            try:
                global INTERVAL
                INTERVAL = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse.create_from_method_request(method_request, response_status, response_payload)
        client.send_method_response(method_response)

    try:
        # Attach the method request handler
        client.on_method_request_received = method_request_handler
    except:
        # Clean up in the event of failure
        client.shutdown()
        raise

    return client


def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    client.connect()

    while True:
        message = Message(read_temp(), content_encoding='utf-8', content_type='application/json')
        print(f'Sending message: {message}')

        # Send the message to Azure IOT
        client.send_message(message)
        print("Message sent")
        time.sleep(TIMING)


def main():
    print ("Press Ctrl-C to exit")
    
    # Instantiate the client. Use the same instance of the client for the duration of
    # your application
    client = create_client()

    # Send telemetry
    try:
        run_telemetry_sample(client)
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        print("Shutting down IoTHubClient")
        client.shutdown()



if __name__ == "__main__":
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")
    TIMING = 300
    
    # These tow lines mount the device:
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    # Get all the filenames begin with 28 in the path base_dir.
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    main()




