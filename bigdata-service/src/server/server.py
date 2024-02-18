from common_modules.rest.server import Server
from common_modules.storage.resource_mgr import ResourceMgr
from common_modules.logger.mnt_logging import MntLogging as MyLog
from common_modules.storage.storage_local import StorageLocal
from src.datamodel.item_info import ItemInfoRequestSchema, ItemInfoRequest, ItemsInfoResponseSchema, ItemsInfoResponse
from src.datamodel.item_info import ItemInfoBulkRequestSchema, ItemInfoBulkRequest, ItemsInfoBulkResponseSchema, \
    ItemsInfoBulkResponse
from src.datamodel.user_activity import UserActivitySchema, UserActivityResponseSchema, UserActivityResponse
from src.datamodel.user_chat_analytics import UserChatAnalyticsSchema
from src.datamodel.user_profile_analytics import UserProfileDataAnalyticsSchema
from src.datamodel.item_info import ItemsInfo
import threading
import json
from json import dumps
from kafka import KafkaProducer
from pdb import set_trace as st

resource_mgr = ResourceMgr(StorageLocal())

kafka_sink_ip = "localhost"
kafka_port = 9092


def send_to_kafka(topic_name, value):
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=[f'{kafka_sink_ip}:{kafka_port}'])

    producer.send(topic_name, value=value)
    producer.flush()


def get_item_info(item_id: int):
    resp = resource_mgr.read("item_normalization_table_etl_new", str(item_id))[0]
    MyLog().getlogger().debug(resp)
    items_info_response = ItemsInfoResponse(item_id=item_id,
                                            item_id_info=ItemsInfo(name=resp['name'], url=resp['url'],
                                                                   description=resp['description'],
                                                                   provider=resp['provider'], online=resp['online'],
                                                                   paid=resp['online'], upvotecount=resp['upvotecount'],
                                                                   downvotecount=resp['downvotecount'],
                                                                   sharecount=resp['sharecount'],
                                                                   tags=resp['tags']))
    return items_info_response


def item_info_get_handler(request_obj):
    item_id = request_obj.item_id
    return get_item_info(item_id)


def item_info_bulk_get_handler(request_obj):
    item_id_list = request_obj.item_id_list
    response = []
    for item in item_id_list:
        response.append(get_item_info(item.item_id))
    return ItemsInfoBulkResponse(item_list_info=response)


def rest_server_item_info_handler(thr_id: int, name, port: int, host, resmgr: ResourceMgr):
    """
    This is the rest server thread
    """

    global resource_mgr
    resource_mgr = resmgr
    server_item_info = Server(name=name, port=port, debug=False, host=host)
    server_item_info.add_endpoint(endpoint=name,
                                  get_request_schema=ItemInfoBulkRequestSchema(),
                                  get_response_schema=ItemsInfoBulkResponseSchema(),
                                  get_handler=item_info_bulk_get_handler)
    server_item_info.run()


def user_activity_handler(request_obj):
    MyLog().getlogger().debug(f"user_activity_handler invoked {request_obj}")
    send_to_kafka("user-activity", UserActivitySchema().dump(request_obj))
    return UserActivityResponse(user_id=request_obj.user_id, status="Success")


def rest_server_user_activity_handler(thr_id: int, name, port: int, host, resmgr: ResourceMgr):
    """
    This is the rest server thread
    """
    server_item_info = Server(name=name, port=port, debug=False, host=host)
    server_item_info.add_endpoint(endpoint=name,
                                  get_request_schema=UserActivitySchema(),
                                  get_response_schema=UserActivityResponseSchema(),
                                  get_handler=user_activity_handler)
    server_item_info.run()


def user_chat_analytics_handler(request_obj):
    MyLog().getlogger().debug(f"user_chat_analytics_handler invoked {request_obj}")
    send_to_kafka("user-chat-analytics", UserChatAnalyticsSchema().dump(request_obj))
    return UserActivityResponse(user_id=request_obj.user_id, status="Success")


def rest_server_user_chat_analytics_handler(thr_id: int, name, port: int, host, resmgr: ResourceMgr):
    """
    This is the rest server thread
    """
    server_item_info = Server(name=name, port=port, debug=False, host=host)
    server_item_info.add_endpoint(endpoint=name,
                                  get_request_schema=UserChatAnalyticsSchema(),
                                  get_response_schema=UserActivityResponseSchema(),
                                  get_handler=user_chat_analytics_handler)
    server_item_info.run()


def user_profile_analytics_handler(request_obj):
    MyLog().getlogger().debug(f"user_profile_analytics_handler invoked {request_obj}")
    send_to_kafka("user-profile-analytics", UserProfileDataAnalyticsSchema().dump(request_obj))
    return UserActivityResponse(user_id=request_obj.user_id, status="Success")


def rest_server_user_profile_analytics_handler(thr_id: int, name, port: int, host, resmgr: ResourceMgr):
    """
    This is the rest server thread
    """
    server_item_info = Server(name=name, port=port, debug=False, host=host)
    server_item_info.add_endpoint(endpoint=name,
                                  get_request_schema=UserProfileDataAnalyticsSchema(),
                                  get_response_schema=UserActivityResponseSchema(),
                                  get_handler=user_profile_analytics_handler)
    server_item_info.run()


def start_rest_server(conf_file, resmgr: ResourceMgr):
    file = open('config/' + conf_file)
    config_data = json.load(file)
    MyLog().getlogger().debug(f"Config is {config_data}")
    global kafka_port
    kafka_port = config_data['kafka-port']
    global kafka_sink_ip
    kafka_sink_ip = config_data['kafka-sink-ip']
    thread_pool = []
    for server in config_data['servers']:
        if server['name'] == "bigdata-get-bulk-item-info":
            thr = threading.Thread(target=rest_server_item_info_handler,
                                   args=(1, server['name'], server['port'],
                                         server['host'], resmgr),
                                   daemon=True)
            thr.start()
            thread_pool.append(thr)
        elif server['name'] == "user-activity":
            thr = threading.Thread(target=rest_server_user_activity_handler,
                                   args=(2, server['name'], server['port'],
                                         server['host'], resmgr),
                                   daemon=True)
            thr.start()
            thread_pool.append(thr)
        elif server['name'] == "user-chat-analytics":
            thr = threading.Thread(target=rest_server_user_chat_analytics_handler,
                                   args=(1, server['name'], server['port'],
                                         server['host'], resmgr),
                                   daemon=True)
            thr.start()
            thread_pool.append(thr)
        elif server['name'] == "user-profile-analytics":
            thr = threading.Thread(target=rest_server_user_profile_analytics_handler,
                                   args=(1, server['name'], server['port'],
                                         server['host'], resmgr),
                                   daemon=True)
            thr.start()
            thread_pool.append(thr)
        else:
            MyLog().getlogger().error("Unsupported Rest server type")

    for thr in thread_pool:
        thr.join()
