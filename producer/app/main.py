import asyncio
import os
import time

from fastapi import FastAPI
from ProducerInterface import ProducerInterface
from GPSCoordinates import GPSTracker
import logging
logging.basicConfig(level=logging.INFO)

print("Launching app")
app = FastAPI()


@app.on_event('startup')
async def main_loop():
    logging.info('Starting up producer')
    conf = {
        'kafka_host': os.environ.get('KAFKA_HOST'),
        'client_id': os.environ.get('HOSTNAME'),
        'topic': os.environ.get('TOPIC'),
    }
    producer = ProducerInterface(conf)
    logging.info('Starting up GPS tracker')
    gps_tracker = GPSTracker()
    while True:
        gps_tracker.update()
        data = {
                "id": conf['client_id'],
                "longitude": gps_tracker.get_gps_coordinates().longitude,
                "latitude": gps_tracker.get_gps_coordinates().latitude,
                "date": int(gps_tracker.datetime.timestamp() * 1_000),
        }
        producer.produce(data)
        logging.info(f"SEND {data}")
        time.sleep(0.33)
