import asyncio
import os

from fastapi import FastAPI
# from ProducerInterface import ProducerInterface
from GPSCoordinates import GPSTracker
import logging
logging.basicConfig(level=logging.INFO)


conf = {
    'kefka_host': os.environ.get('KAFKA_HOST'),
    'client_id': os.environ.get('CLIENT_ID'),
    'topic': os.environ.get('TOPIC'),
}
print("Launching app")
app = FastAPI()

@app.on_event('startup')
async def main_loop():
    print('Starting up producer')
    # producer = ProducerInterface(conf)
    print('Starting up GPS tracker')
    gps_tracker = GPSTracker()
    while True:
        gps_tracker.update()
        # producer.produce(
        #     gps_tracker.get_gps_coordinates()
        # )
        logging.info(f"Je suis à : {gps_tracker.get_gps_coordinates()}")
        await asyncio.sleep(1)