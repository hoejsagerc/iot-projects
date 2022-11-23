FROM python:3.8.13

LABEL Maintainer="ScriptingChris"

WORKDIR /app

COPY ./sensor.py /app/sensor.py

RUN pip3 install azure-iot-device 

CMD ["python", "-u", "sensor.py"]
