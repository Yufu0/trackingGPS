import json

from confluent_kafka import Producer


class ProducerInterface(object):
    def __init__(self, conf: dict):
        self.kafka_host = conf['kafka_host']
        self.client_id = conf['client_id']
        self.topic = conf['topic']

        producer_conf = {
            'bootstrap.servers': self.kafka_host,
            'client.id': self.client_id,
        }
        self.producer = Producer(producer_conf)

    def produce(self, data: dict):
            try:
                data = json.dumps(data).encode('utf-8')
                self.producer.produce(
                    self.topic,
                    value=data
                )
                self.producer.flush()
                return {"status": "success", "message": data}
            except Exception as e:
                return {"status": "error", "message": str(e)}



