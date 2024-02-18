from flask import Flask, abort
from http import HTTPStatus
from flask_restful import Api, Resource, abort

class Server:
    def __init__(self, name: str, host: str, port: int, debug: bool):
        self.app = Flask(name)
        self.port = port
        self.debug = debug
        self.api = Api(self.app)
        self.host = host
    
    # Function to kick start the server.
    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)
    
    # Use this function to associate get/put/delete schema and handler to a server endpoint.
    # Full HTTP URL format: http://<server address>:<server port>/<endpoint>/<request>
    # <request> is the dumped JSON request schema string.
    def add_endpoint(self, endpoint,
                     get_request_schema=None, get_response_schema=None, get_handler=None,
                     put_request_schema=None, put_response_schema=None, put_handler=None,
                     delete_request_schema=None, delete_response_schema=None, delete_handler=None):
        self.api.add_resource(Server_handler_, f"/{endpoint}/<string:request>",
                              resource_class_kwargs={"get_request_schema" : get_request_schema, "get_response_schema" : get_response_schema, "get_handler" : get_handler,
                                                     "put_request_schema" : put_request_schema, "put_response_schema" : put_response_schema, "put_handler" : put_handler,
                                                     "delete_request_schema" : delete_request_schema, "delete_response_schema" : delete_response_schema, "delete_handler": delete_handler})


class Server_handler_(Resource):
    def __init__(self,
                 get_request_schema, get_response_schema, get_handler,
                 put_request_schema, put_response_schema, put_handler,
                 delete_request_schema, delete_response_schema, delete_handler):
        self.get_request_schema = get_request_schema
        self.get_response_schema = get_response_schema
        self.get_handler = get_handler
        self.put_request_schema = put_request_schema
        self.put_response_schema = put_response_schema
        self.put_handler = put_handler
        self.delete_request_schema = delete_request_schema
        self.delete_response_schema = delete_response_schema
        self.delete_handler = delete_handler
    
    def get(self, request):
        return self.handle(request, self.get_request_schema, self.get_response_schema, self.get_handler)
        
    def put(self, request):
        return self.handle(request, self.put_request_schema, self.put_response_schema, self.put_handler)
    
    def delete(self, request):
        return self.handle(request, self.delete_request_schema, self.delete_response_schema, self.delete_handler)
    
    def handle(self, request, requestSchema, responseSchema, handler):
        # If requestSchema does not exist or request does not compline with schema format,
        # return HTTP BAD_REQUEST. Otherwise, deserialize request to request_obj.
        try:
            request_obj = requestSchema.loads(request)
        except:
            abort(HTTPStatus.BAD_REQUEST)

        # Any failure after validation of request is considered INTERNAL_SERVER_ERROR.
        # Use handler callback to process request_obj. Serialize response_obj before reply.
        try:
            response_obj = handler(request_obj)
            # TODO: handle if some handle does not have response schema, return a simple status code.
            response = responseSchema.dump(response_obj)
            return response
        except:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
