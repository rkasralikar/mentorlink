"""  Items class for Kafka Service
Author: Sudipto Nandi

Copyrights: MentorLink 2021-2022

Description: This class implements
the Kafka service
"""
import json
from time import sleep
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.storage.storage_local import StorageLocal
from src.datamodel.user_activity import UserActivitySchema
from src.datamodel.user_chat_analytics import UserChatAnalyticsSchema
from src.datamodel.user_profile_analytics import UserProfileDataAnalyticsSchema
import threading
from kafka import KafkaConsumer
from json import loads

global_mapping = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            }
        }
    }
}


class KafkaConsumerTask:
    def __init__(self, topic_name=None, elastic_sink_name=None, schema_name=None, bootstrap_server=None,
                 res_mgr=ResourceMgr(StorageLocal()), client_id=None, ssl_ca_file=None,
                 security_protocol=None, sasl=None):
        MyLog().getlogger().debug(f"Ctor topic_name {topic_name} elastic_sink_name {elastic_sink_name} "
                                  f"bootstrap_server {bootstrap_server} client_id {client_id} ssl_ca_file {ssl_ca_file} "
                                  f"security_protocol {security_protocol} sasl {sasl}")
        self.topic_name = topic_name
        self.elastic_sink_name = elastic_sink_name
        self.schema_name = schema_name
        self.bootstrap_server = bootstrap_server
        self.res_mgr = res_mgr
        bootstrap_str = bootstrap_server
        MyLog().getlogger().debug(f"bootstrap_str {bootstrap_str}")
        def deserializer(m):
            try:
                return loads(m.decode('utf-8'))
            except Exception as ex:
                    MyLog().getlogger().error(ex)
                    MyLog().getlogger().error(f"Exception occurred while deserializing message {m}")

        if client_id is not None:
            self.consumer = KafkaConsumer(
                self.topic_name,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda m: deserializer(m),
                bootstrap_servers=bootstrap_str,
                client_id=client_id,
                ssl_cafile=ssl_ca_file,
                security_protocol="PLAINTEXT" if security_protocol is None else security_protocol,
                sasl_mechanism=None if sasl is None else sasl['mechanism'],
                sasl_plain_username=None if sasl is None else sasl['username'],
                sasl_plain_password=None if sasl is None else sasl['password'])
        else:
            self.consumer = KafkaConsumer(
                self.topic_name,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda m: deserializer(m),
                bootstrap_servers=bootstrap_str)

    def start(self):
        MyLog().getlogger().debug(f"Starting kafka consumer task for {self.topic_name}")
        for message in self.consumer:
            MyLog().getlogger().debug(f"Message received for topic {self.topic_name}\tMessage: {message.value}")
            try:
                if '_id' in message.value.keys():
                    del message.value['_id']
                self.res_mgr.add(self.elastic_sink_name, None, message.value, global_mapping)
                self.post_processing(message)
            except Exception as ex:
                MyLog().getlogger().error(ex)
                MyLog().getlogger().error(f"Exception occurred inserting message for topic {self.topic_name}"
                                              f" sink: {self.elastic_sink_name} Message: {message.value}")

    def post_processing(self, message):
        MyLog().getlogger().debug(f"Topic {self.topic_name} has no post processing")


def get_boot_strap_server_string(server_details):
    server_str_list = []
    MyLog().getlogger().debug(f"Server details obtained {server_details}")
    for sd in server_details:
        server_str_list.append(sd['ip'] + ":" + str(sd['port']))
    return ','.join(server_str_list)


def start_kafka_service(config_file=None, res_mgr=None):
    file = open('config/' + config_file)
    config_data = json.load(file)
    MyLog().getlogger().debug(f"Config is {config_data}")
    thread_pool = []
    for topic in config_data['topics']:
        kafka_consume_task = None
        ssl_ca_file = None
        if "ssl_ca_file" in topic.keys():
            ssl_ca_file = topic['ssl_ca_file']
        security_protocol = None
        if "security_protocol" in topic.keys():
            security_protocol = topic['security_protocol']
        sasl = None
        if "sasl" in topic.keys():
            security_protocol = topic['sasl']
        if topic['topic_name'] == 'user-activity':
            kafka_consume_task = KafkaConsumerTask(topic_name=topic['topic_name'],
                                                   elastic_sink_name=topic['sink_table_name'],
                                                   schema_name=UserActivitySchema,
                                                   bootstrap_server=get_boot_strap_server_string(
                                                       topic['bootstrap_server']),
                                                   res_mgr=res_mgr, client_id=topic['client_id'],
                                                   ssl_ca_file=ssl_ca_file,
                                                   security_protocol=security_protocol,
                                                   sasl=sasl
                                                   )
        elif topic['topic_name'] == 'user-chat-analytics':
            kafka_consume_task = KafkaConsumerTask(topic_name=topic['topic_name'],
                                                   elastic_sink_name=topic['sink_table_name'],
                                                   schema_name=UserChatAnalyticsSchema,
                                                   bootstrap_server=get_boot_strap_server_string(
                                                       topic['bootstrap_server']),
                                                   res_mgr=res_mgr, client_id=topic['client_id'],
                                                   ssl_ca_file=ssl_ca_file,
                                                   security_protocol=security_protocol,
                                                   sasl=sasl)
        elif topic['topic_name'] == 'user-profile-analytics':
            kafka_consume_task = KafkaConsumerTask(topic_name=topic['topic_name'],
                                                   elastic_sink_name=topic['sink_table_name'],
                                                   schema_name=UserProfileDataAnalyticsSchema,
                                                   bootstrap_server=get_boot_strap_server_string(
                                                       topic['bootstrap_server']),
                                                   res_mgr=res_mgr, client_id=topic['client_id'],
                                                   ssl_ca_file=ssl_ca_file,
                                                   security_protocol=security_protocol,
                                                   sasl=sasl)
        else:
            MyLog().getlogger().error(f"Topic Name {topic['topic_name']} not supported yet")
            return
        if kafka_consume_task is not None:
            thr = threading.Thread(target=kafka_consume_task.start)
            thread_pool.append(thr)
            thr.start()

    for thr in thread_pool:
        thr.join()
    MyLog().getlogger().debug(f"Kafka Consumer task is over")
