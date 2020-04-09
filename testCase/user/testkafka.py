
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import SimpleProducer
from kafka import KafkaClient
from kafka.errors import KafkaError
import json
import sys


from common import event_pb2 as Protobuf_pb2
from common import enums_pb2  as Enums_pb2
adxEvent = Protobuf_pb2.AdxEvent
pubRequest = Enums_pb2.EventType
carrier = Enums_pb2.Carrier
connectionType=Enums_pb2.ConnectionType
valid = Enums_pb2.ValidType
os_type = Enums_pb2.OSType
adType = Enums_pb2.AdType
biddingType = Enums_pb2.BiddingType
pubApiType = Enums_pb2.PubApiType
dspApiType = Enums_pb2.DspApiType
dealType = Enums_pb2.DealType
creativeType = Enums_pb2.CreativeType
interactionType = Enums_pb2.InteractionType
useType = Enums_pb2.UseType
dropType = Enums_pb2.DropType
agImp2ConfigType = Enums_pb2.AgImp2ConfigType



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
            # parmas_message = json.dumps(params)
            parmas_message=str(params)
            # parmas_message=None
            producer = self.producer
            # producer.send(self.kafkatopic, parmas_message.encode('utf-8'))
            producer.send(self.kafkatopic,parmas_message.encode('utf-8'))
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
            kafka_port=self.kafkaPort ),heartbeat_interval_ms=2000,session_timeout_ms=6000)
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
    producer = Kafka_producer("adx61", 9092, "c1")
    for id in range(1):
        params=adxEvent(timestamp0=1564985539000,
                        timestamp=1564985539000,
                        request_id="554af654-99f1-4de2-9663-65d4f487f29a",
                        event_type=pubRequest.PUBLISHER_REQUEST,
                        api_version="10",
                        carrier=carrier.CHINA_MOBILE,
                        mcc="864230036377784",
                        ip="199.168.0.66",
                        longitude=113.944334,
                        latitude=22.544177,
                        device_model="NEM-AL10",
                        conection_type=connectionType.WIFI,
                        os_type=os_type.ANDROID,
                        idfa="864230036377732",
                        imei="834230036377784",
                        imsi="",
                        device_id="834230036377114",
                        mac="44:c3:46:f4:6b:05",
                        ua="Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
                        ad_type=adType.BANNER,
                        pub_app_ad_id=991,
                        pub_app_id=419,
                        pub_id=268,
                        dsp_app_id=0,
                        dsp_id=0,
                        dsp_code=69,
                        pub_api_type=pubApiType.PUB_S2S,
                        dsp_api_type=dspApiType.S2S,
                        deal_type=dealType.CPM,
                        ecpm=0.0,
                        deal_price=0.0,
                        amount=0.0,
                        ad_creative_type=creativeType.IMAGE_TEXT,
                        ad_interaction_type=interactionType.NO_INTERACTION,
                        ad_title="test",
                        ad_package_name="com.zzcm.wtwd",
                        impression_type=0,
                        imp_expire_at=1564986019000,
                        click_expire_at=1564986019000,
                        ad_img_url="http://sf1-ttcdn-tos.pstatp.com/img/ad.union.api/55da.jpeg",
                        ad_icon_url="http://sf1-ttcdn-tos.pstatp.com/img/ad.union.api/55da2b3e556fc1bfeeb01c5cb484ecc9~cs_640x100_q75.jpeg",
                        ad_deeplink_url="",
                        ad_target_url="",
                        ad_download_url="https://lf.snssdk.com/api/ad/union/redirect/?req_id=31c5f380-dabc-4e3a-bcdb-8247c352u1271&use_pb=1&rit=900547722&call_back=%2BH2%2Bub8Mm4BjLmXWvI68IwDA",
                        ad_redirect_download_url="",
                        ad_html="",
                        use_type=useType.SELF,
                        is_video_ad=False,
                        ad_channel_id=645,
                        mid="ssiddca98c74423142258b994801ed9f779f",
                        ad_group_id=46,
                        ad_customer_id=14257,
                        ad_template_id=0,
                        is_ag_app=True)
        # params = '{abetst}:{null}---'+str(id)
        producer.sendjsondata(params)
    ##测试消费模块
    #消费模块的返回格式为ConsumerRecord(topic=u'ranktest', partition=0, offset=202, timestamp=None,
    #\timestamp_type=None, key=None, value='"{abetst}:{null}---0"', checksum=-1868164195,
    #\serialized_key_size=-1, serialized_value_size=21)
    #
    # consumer = Kafka_consumer('adx61', 9092, "c1", 'group-stats')
    # message = consumer.consume_data()
    # for i in message:
    #     print(i.value)


if __name__ == '__main__':
    main()