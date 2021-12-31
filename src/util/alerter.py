import json
import time
from confluent_kafka import Producer
from src.db.soul import SoulDB

class KafkaProducer:
    _kafka_producer = None
    _meta_db = None

    @classmethod
    def _get_user_mails(cls):
        if not cls._meta_db:
            db = SoulDB.get_prod_db()
            cls._meta_db = db['meta']
        col_devops_rotation = cls._meta_db.get_collection('devopsRotation')
        col_soul_users = cls._meta_db.get_collection('soulUsers')
        user_ids = list(col_devops_rotation.find({'activation': True}, {'userId': True}))
        user_ids = list(map(lambda el: el.get('userId'), user_ids))
        mails = list(col_soul_users.find({'userId': {'$in': user_ids}}, {'daouofficeEmail': True}))
        mails = list(map(lambda el: el.get('daouofficeEmail'), mails))
        return mails

    @classmethod
    def _get_kafka_producer_obj(cls):
        if not cls._kafka_producer:
            cls._kafka_producer = Producer({
            'bootstrap.servers': '{kafka brokers}',
            'compression.type': 'lz4'
        })
        return cls._kafka_producer

    @classmethod
    def alert(cls, flow_name, message):
        content = {
            'text': f'NINES FLOW failed {flow_name}',
            'blocks': [{
                'type': 'header',
                'text': 'NINES FLOW Alert',
                'style': 'yellow'
            }, {
                "type": "text",
                "text": "-",
                "inlines": [{
                    "type": "styled",
                    "text": f"{flow_name} failed",
                    "bold": True
                }]
            }, {
                "type": "text",
                "text": message
            }]
        }
        mails = cls._get_user_mails()
        for mail in mails:
            kafka_doc = {
                "messageType": "message",
                "timestamp": int(time.time()),
                "data": {
                    "messageType": "alert",
                    "title": "NINES FLOW Alert",
                    "content": content,
                    "reservationTime": None,
                    "targets": [{
                        "userId": "devops",
                        "channel": "kakaowork",
                        "to": mail
                    }],
                    "data": {}
                }
            }
            res = cls.publish('Message', kafka_doc)

    @classmethod
    def publish(cls, topic, message):
        kafka_producer = cls._get_kafka_producer_obj()
        try:
            kafka_producer.produce(topic, json.dumps(message))
            kafka_producer.poll(timeout=0.3)
            return True
        except Exception as e:
            return False