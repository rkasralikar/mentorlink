from sample_get_request import SampleGetRequest, SampleGetRequestSchema
from sample_get_response import SampleGetResponse, SampleGetResponseSchema
from common_modules.rest.client import Client

def get(request : SampleGetRequest) -> SampleGetResponse:
    sample_client = Client(addr="localhost", port="5000", endpoint="sample-endpoint", get_request_schema=SampleGetRequestSchema(), get_response_schema=SampleGetResponseSchema())
    return sample_client.get(request)


if __name__ == "__main__":
    sample_get_request = SampleGetRequest(type="I am a sample request", field1="aaaaaaaa", field2="sssssssss")
    sample_get_response = get(sample_get_request)
    print(f"type:{sample_get_response.type}, field1:{sample_get_response.field1}, field2:{sample_get_response.field2}")