from common_modules.rest.server import Server
from src.datamodel.recommendation_response import RecommendationResponse, RecommendationResponseSchema
from src.datamodel.recommendation_response import RecommendationRequest, RecommendationRequestSchema
from src.user.user import User
import threading
import time
import concurrent.futures
from pdb import set_trace as st
from common_modules.logger.mnt_logging import MntLogging as MyLog
from src.recomgr.reco_mgr import RecommendationMgr


def recommendation_get_handler(request_obj):
    interest_list = []
    MyLog().getlogger().debug(f"Recommendation API has been called user:{request_obj.user_id} interest_list: {request_obj.interest_list}")
    if len(request_obj.interest_list) != 0:
        for interest in request_obj.interest_list:
            inter = interest.split(',')
            if type(inter) == list:
                for i in inter:
                    interest_list.append(i)
            else:
                interest_list.append(inter)
    MyLog().getlogger().debug(f"Responding to the recommendation request for user {request_obj.user_id} interest_list {interest_list}")

    sample_response = RecommendationResponse(user_id=request_obj.user_id,
                                             item_id_info=RecommendationMgr().get_recommendation_for_user(
                                                 user_id=str(request_obj.user_id)))
    return sample_response


def rest_server_handler(thr_id, host, port):
    MyLog().getlogger().debug("Rest server thread({}) has started".format(thr_id))
    server = Server(name="recommendation-service", host=host, port=port, debug=False)
    server.add_endpoint(endpoint="recommendation",
                        get_request_schema=RecommendationRequestSchema(),
                        get_response_schema=RecommendationResponseSchema(),
                        get_handler=recommendation_get_handler)
    server.run()


def start_rest_server(port=9011, host="0.0.0.0"):
    MyLog().getlogger().debug("Starting the thread for rest server")
    thr = threading.Thread(target=rest_server_handler, args=(1, host, port))
    thr.start()


if __name__ == "__main__":
    MyLog().setloglevel('debug')
    start_rest_server()
