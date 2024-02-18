from analytics_get_request import AnalyticsGetRequest, AnalyticsGetRequestSchema
from analytics_get_response import AnalyticsGetResponse, AnalyticsGetResponseSchema
from common_modules.rest.client import Client

def get(request : AnalyticsGetRequest) -> AnalyticsGetResponse:
    analytics_client = Client(addr="localhost", port="5000", endpoint="analytics", get_request_schema=AnalyticsGetRequestSchema(), get_response_schema=AnalyticsGetResponseSchema())
    return analytics_client.get(request)


if __name__ == "__main__":
    analytics_get_request = AnalyticsGetRequest(type="USER", entity="0252342", keys=["pages.visited"], reduce="top(10)", start_time="2020-01-01", end_time="now")
    analytics_get_response = get(analytics_get_request)
    print(f"type:{analytics_get_response.type}, entity:{analytics_get_response.entity}, data:{analytics_get_response.data}")