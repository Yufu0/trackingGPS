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
    'kafka_host': '172.19.0.3:9092',
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
    if True:
        gps_tracker.update()
        producer.produce(
            gps_tracker.get_gps_coordinates()
        )
        logging.info(f"SEND")
        # logging.info(f"Je suis à : {gps_tracker.get_gps_coordinates()}")
        await asyncio.sleep(1)




from confluent_kafka import Consumer
@app.on_event('startup')
async def main_loop2():
    c = Consumer({
        'bootstrap.servers': '172.19.0.3:9092',
        'group.id': '1',
        'auto.offset.reset': 'earliest'
    })

    c.subscribe(['coordinates'])
    producer = ProducerInterface(conf)

    from time import time

    while True:
        a = time()
        producer.produce(
            {"a": str(a)}
        )
        logging.info(f"SEND")
        await asyncio.sleep(1)
        msg = c.poll(1.0)

        if msg is None:
            logging.info("No message received by consumer")
            continue
        if msg.error():
            logging.info("Consumer error: {}".format(msg.error()))
            continue

        logging.info(f'Received message: {msg.value()} {time()}')

    c.close()