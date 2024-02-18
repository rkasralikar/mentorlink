from insights_get_request import InsightsGetRequest, InsightsGetRequestSchema
from insights_get_response import InsightsGetResponse, InsightsGetResponseSchema
from common_modules.rest.client import Client

def get(request : InsightsGetRequest) -> InsightsGetResponse:
    insights_client = Client(addr="localhost", port="5000", endpoint="insights", get_request_schema=InsightsGetRequestSchema(), get_response_schema=InsightsGetResponseSchema())
    return insights_client.get(request)


if __name__ == "__main__":
    insights_get_request = InsightsGetRequest(user_id=252342, history_window="1m")
    insights_get_response = get(insights_get_request)
    print(f"user_id:{insights_get_response.user_id}, history_window:{insights_get_response.history_window}")
    for ui in insights_get_response.user_insights:
        print(f"interest:{ui.interest}, # read:{ui.n_read}, # liked:{ui.n_liked}, # saved:{ui.n_saved}, # shared:{ui.n_shared}")
