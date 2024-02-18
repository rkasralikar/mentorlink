import json
import requests

class Client:
    # Full HTTP URL format: http://<server address>:<server port>/<endpoint>/<request>
    # <request> is the dumped JSON request schema string.
    def __init__(self, addr: str, port: int, endpoint: str,
                 get_request_schema=None, get_response_schema=None,
                 put_request_schema=None, put_response_schema=None,
                 delete_request_schema=None, delete_response_schema=None):
        self.addr = addr
        self.port = port
        self.endpoint = endpoint
        self.get_request_schema = get_request_schema
        self.get_response_schema = get_response_schema
        self.put_request_schema = put_request_schema
        self.put_response_schema = put_response_schema
        self.delete_request_schema = delete_request_schema
        self.delete_response_schema = delete_response_schema

    def get(self, request):
        return self.handle(request, self.get_request_schema, self.get_response_schema)

    def put(self, request):
        return self.handle(request, self.put_request_schema, self.put_response_schema)

    def delete(self, request):
        return self.handle(request, self.delete_request_schema, self.delete_response_schema)
    
    def handle(self, request, requestSchema, responseSchema):
        try:
            # TODO(fcdu) json.dumps replace single quotation with double quotation
            # marshmallow serialization and deserialization use double quotation
            request_json = json.dumps(requestSchema.dump(request))
            request_url = f"http://{self.addr}:{self.port}/{self.endpoint}/{request_json}"
            response_json = json.dumps(requests.get(request_url).json())
            return responseSchema.loads(response_json)
        except:
            print("Error in handling request.")
            return None
