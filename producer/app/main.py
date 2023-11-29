import asyncio
import os

from fastapi import FastAPI
from ProducerInterface import ProducerInterface
from GPSCoordinates import GPSTracker
import logging
logging.basicConfig(level=logging.INFO)


conf = {
    'kafka_host': os.environ.get('KAFKA_HOST'),
    'client_id': os.environ.get('CLIENT_ID'),
    'topic': os.environ.get('TOPIC'),
}

print("Launching app")
app = FastAPI()

@app.on_event('startup')
async def main_loop():
    logging.info('Starting up producer')
    producer = ProducerInterface(conf)
    logging.info('Starting up GPS tracker')
    gps_tracker = GPSTracker()
    if True:
        gps_tracker.update()
        producer.produce(
            gps_tracker.get_gps_coordinates()
        )
        logging.info(f"Sending coordinates: {gps_tracker.get_gps_coordinates()})
        await asyncio.sleep(1)