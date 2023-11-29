import asyncio
import os

from fastapi import FastAPI
from ProducerInterface import ProducerInterface
from GPSCoordinates import GPSTracker
import logging
logging.basicConfig(level=logging.INFO)

print("Launching app")
app = FastAPI()

#
# @app.on_event('startup')
# async def main_loop():
#     logging.info('Starting up producer')
#     # conf = {
#     #     'kafka_host': os.environ.get('KAFKA_HOST'),
#     #     'client_id': os.environ.get('CLIENT_ID'),
#     #     'topic': os.environ.get('TOPIC'),
#     # }
#     conf = {
#         'kafka_host': '172.17.4.182:29092',
#         'client_id': '1',
#         'topic': 'coordinates',
#     }
#     producer = ProducerInterface(conf)
#     logging.info('Starting up GPS tracker')
#     gps_tracker = GPSTracker()
#     while True:
#         gps_tracker.update()
#         producer.produce(
#             {
#                 "id": conf['client_id'],
#                 "longitude": gps_tracker.get_gps_coordinates().longitude,
#                 "latitude": gps_tracker.get_gps_coordinates().latitude,
#                 "date": str(gps_tracker.datetime),
#             }
#         )
#         logging.info(f"SEND")
#         # logging.info(f"Je suis à : {gps_tracker.get_gps_coordinates()}")
#         await asyncio.sleep(1)


from confluent_kafka import Consumer
from time import time


@app.on_event('startup')
async def main_loop2():
    c = Consumer({
        'bootstrap.servers': '0.0.0.0:29092',
        'group.id': '1',
        'auto.offset.reset': 'earliest'
    })

    c.subscribe(['coordinates'])
    producer = ProducerInterface({
        'kafka_host': '0.0.0.0:29092',
        'client_id': '1',
        'topic': 'coordinates',
    })
    gps_tracker = GPSTracker()

    while True:
        gps_tracker.update()
        producer.produce(
            {
                "id": '1',
                "longitude": gps_tracker.get_gps_coordinates().longitude,
                "latitude": gps_tracker.get_gps_coordinates().latitude,
                "date": str(gps_tracker.datetime),
            }
        )
        logging.info(f"SEND")

        msg = c.poll(1.0)

        if msg is None:
            logging.info("No message received by consumer")
            continue
        if msg.error():
            logging.info("Consumer error: {}".format(msg.error()))
            continue

        logging.info(f'Received message: {msg.value()} {time()}')
        await asyncio.sleep(1)

    c.close()