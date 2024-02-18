from common_modules.rest.server import Server
from schema.sample.sample_get_request import SampleGetRequestSchema
from schema.sample.sample_get_response import SampleGetResponseSchema, SampleGetResponse
import threading


def sample_get_handler(sample_get_request):
    sample_get_response = SampleGetResponse(type="I am a sample response",
                                            field1=sample_get_request.field1,
                                            field2=sample_get_request.field2)
    return sample_get_response


def rest_server_handler():
    '''
    Start the data gathering thread
    Start feature extraction
    Start model Training
    Start the rest server
    '''
    # Sample Test URL:
    # http://127.0.0.1:5000/sample-endpoint/{"field2": "ghijkl", "field1": "abcdef", "type": "I am a sample Request"}
    server = Server(name="sample-micro-service", port=5000, debug=False)
    server.add_endpoint(endpoint="sample-endpoint",
                        get_request_schema=SampleGetRequestSchema(),
                        get_response_schema=SampleGetResponseSchema(),
                        get_handler=sample_get_handler)
    server.run()


def start_rest_server():
    thr = threading.Thread(target=rest_server_handler, args=())
    thr.start()

"""
Testing purpose
"""
if __name__ == "__main__":
    start_rest_server()
