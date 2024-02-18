from common_modules.rest.server import Server
from schema.insights.insights_get_request import InsightsGetRequest, InsightsGetRequestSchema
from schema.insights.insights_get_response import InsightsGetResponse, InsightsGetResponseSchema, NudgesStats
import threading


def insights_get_handler(insights_get_request: InsightsGetRequest) -> InsightsGetResponse:
    n1 = NudgesStats(interest="Basketball", n_read=13, n_liked=9, n_shared=8, n_saved=5)
    n2 = NudgesStats(interest="C++", n_read=34, n_liked=29, n_shared=28, n_saved=25)
    n3 = NudgesStats(interest="Mentorlink", n_read=65, n_liked=45, n_shared=44, n_saved=40)
    insights_get_response = InsightsGetResponse(user_id=insights_get_request.user_id,
                                                history_window=insights_get_request.history_window,
                                                user_insights=[n1, n2, n3])
    return insights_get_response


def rest_server_handler():
    '''
    Start the data gathering thread
    Start feature extraction
    Start model Training
    Start the rest server
    '''
    server = Server(name="insights-service", host='0.0.0.0', port=9001, debug=False)
    server.add_endpoint(endpoint="insights",
                        get_request_schema=InsightsGetRequestSchema(),
                        get_response_schema=InsightsGetResponseSchema(),
                        get_handler=insights_get_handler)
    server.run()


def start_rest_server():
    thr = threading.Thread(target=rest_server_handler, args=())
    thr.start()

"""
Testing purpose
"""
if __name__ == "__main__":
    start_rest_server()
