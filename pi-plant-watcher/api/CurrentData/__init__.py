import logging
import json
import os
import random
import datetime
from datetime import timedelta
import azure.functions as func
from azure.data.tables import TableClient


CONNECTION_STRING = os.getenv('CONNECTION_STRING')
TABLE_NAME = "PlantData"

# Function for finding the lates entry from the last hour
def find_latest_entry(data_object):
    logtime = list()
    logging.info(f'JsonObject: {data_object}')
    for i in data_object:
        logging.info(f'Logtime: {i}')
        logtime.append(i['LogTime'])

    latest_entry= max(logtime)
    for entry in data_object:
        if entry['LogTime'] == latest_entry:
            return entry


def main(req: func.HttpRequest) -> func.HttpResponse:
    run_id = str(random.randint(1000,9999))
    logging.info(f'{run_id} | API Resource: [GET] - /v1/current_data was triggered')

    # Finding the current time in UTC
    current_utc = datetime.datetime.utcnow()
    from_time = current_utc - timedelta(hours=1)
    from_iso_time = from_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    to_iso_time = current_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    logging.info(f'{run_id} | Created from timeobject: {from_iso_time}')
    logging.info(f'{run_id} | Created to timeobject: {to_iso_time}')

    # Querying the database for all entries in the last hour
    query = f"PartitionKey eq 'rpi-chili' and Timestamp ge datetime'{from_iso_time}' and Timestamp lt datetime'{to_iso_time}'"
    table_client = TableClient.from_connection_string(conn_str=CONNECTION_STRING, table_name=TABLE_NAME)
    entities = table_client.query_entities(query)
    data_object = []
    for entity in entities:
        entity_object = {}
        for key in entity.keys():
            entity_object[key] = entity[key]
            logging.info(f"{run_id} | Key: {key}, Value: {entity[key]}")
        
        data_object.append(entity_object)


    if len(data_object) >= 1:
        return_object = json.dumps(find_latest_entry(data_object))
        return func.HttpResponse(
            return_object,
            status_code=200
        )
    else:
        return func.HttpResponse(
            "No current data was found",
            status_code=404
        )