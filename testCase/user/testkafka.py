from testCase.user import testprotobuf
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import KafkaClient
from kafka.errors import KafkaError
import json


from common import protobuf_pb2 as Protobuf_pb2
adxEvent = Protobuf_pb2.AdxEvent()
adxEvent.ip = "199.168.0.66"
adxEvent.mac = "98:6c:f5:26:6a:d3"
print("aaaaaaaaaaaaa", adxEvent)

KAFKA_HOST = "adx61"
KAFKA_PORT = 9092
KAFKA_TOPIC = "my-topic"



class Kafka_producer():
    '''
    使用kafka的生产模块
    '''

    def __init__(self, kafkahost,kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort
            ))

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafkatopic, parmas_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print(e)


class Kafka_consumer():
    '''
    使用Kafka—python的消费模块
    '''

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid,
                                      bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort ))
        print("可消费的偏移量",self.consumer.beginning_offsets(self.consumer.assignment()))


    def consume_data(self):
        try:
            for message in self.consumer:
                # print json.loads(message.value)
                yield message
        except KeyboardInterrupt as e:
            print(e)


def main():
    '''
    测试consumer和producer
    :return:
    '''
    ##测试生产模块
    producer = Kafka_producer("adx61", 9092, "jiaojiaotest")
    for id in range(10):
       params = '{abetst}:{null}---'+str(id)
       producer.sendjsondata(params)
    ##测试消费模块
    #消费模块的返回格式为ConsumerRecord(topic=u'ranktest', partition=0, offset=202, timestamp=None,
    #\timestamp_type=None, key=None, value='"{abetst}:{null}---0"', checksum=-1868164195,
    #\serialized_key_size=-1, serialized_value_size=21)

    consumer = Kafka_consumer('adx61', 9092, "jiaojiaotest", 'test-python-ranktest')
    message = consumer.consume_data()
    for i in message:
        print(i.value)


if __name__ == '__main__':
    main()