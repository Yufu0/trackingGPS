import asyncio
import os

from fastapi import FastAPI
from ProducerInterface import ProducerInterface
from GPSCoordinates import GPSTracker
import logging
logging.basicConfig(level=logging.INFO)


# conf = {
#     'kafka_host': os.environ.get('KAFKA_HOST'),
#     'client_id': os.environ.get('CLIENT_ID'),
#     'topic': os.environ.get('TOPIC'),
# }

conf = {
    'kafka_host': '0.0.0.0:9092',
    'client_id': '1',
    'topic': 'coordinates',
}


print("Launching app")
app = FastAPI()

@app.on_event('startup')
async def main_loop():
    logging.info('Starting up producer')
    producer = ProducerInterface(conf)
    logging.info('Starting up GPS tracker')
    gps_tracker = GPSTracker()
    while True:
        gps_tracker.update()
        producer.produce(
            {
                "id": conf['client_id'],
                "longitude": gps_tracker.get_gps_coordinates().longitude,
                "latitude": gps_tracker.get_gps_coordinates().latitude,
                "date": str(gps_tracker.datetime),
            }
        )
        logging.info(f"SEND")
        # logging.info(f"Je suis à : {gps_tracker.get_gps_coordinates()}")
        await asyncio.sleep(1)

