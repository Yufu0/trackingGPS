import asyncio
import os
import random

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
        producer.produce(
            {
                "id": conf['client_id'],
                "longitude": gps_tracker.get_gps_coordinates().longitude,
                "latitude": gps_tracker.get_gps_coordinates().latitude,
                "date": int(gps_tracker.datetime.timestamp() * 1000),
            }
        )
        logging.info(f"SEND {conf['client_id']}")
        # logging.info(f"Je suis à : {gps_tracker.get_gps_coordinates()}")
        await asyncio.sleep(1)

#
# from confluent_kafka import Consumer
# from time import time
#
#
# @app.on_event('startup')
# async def main_loop2():
#     c = Consumer({
#         'bootstrap.servers': '0.0.0.0:29093',
#         'group.id': '2',
#         'auto.offset.reset': 'earliest'
#     })
#
#     c.subscribe(['coordinates'])
#     producer = ProducerInterface({
#         'kafka_host': '0.0.0.0:29092',
#         'client_id': '2',
#         'topic': 'coordinates',
#     })
#     gps_tracker = GPSTracker()
#     import time
#     while True:
#         gps_tracker.update()
#         producer.produce(
#             {
#                 "id": '2',
#                 "longitude": gps_tracker.get_gps_coordinates().longitude,
#                 "latitude": gps_tracker.get_gps_coordinates().latitude,
#                 "date": int(gps_tracker.datetime.timestamp() * 1000),
#             }
#         )
#         logging.info(f"SEND {int(time.perf_counter() * 1000)}", )
#         #
#         # msg = c.poll(1.0)
#         #
#         # if msg is None:
#         #     logging.info("No message received by consumer")
#         #     continue
#         # if msg.error():
#         #     logging.info("Consumer error: {}".format(msg.error()))
#         #     continue
#         #
#         # logging.info(f'Received message: {msg.value()}')
#         await asyncio.sleep(0.001)
#
#     c.close()