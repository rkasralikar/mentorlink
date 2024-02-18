from marshmallow import Schema, fields, post_load
import json

########################################
#                                      #
#             Schema Class             #
#                                      #
########################################

class InsightsGetRequestSchema(Schema):
    user_id = fields.Int()
    history_window = fields.Str()

    @post_load
    def create(self, data, **kwargs):
        return InsightsGetRequest(**data)

########################################
#                                      #
#             Model  Class             #
#                                      #
########################################

class InsightsGetRequest:
    def __init__(self, user_id: int, history_window: str):
        self.user_id = user_id
        self.history_window = history_window

########################################
#                                      #
#              Validator               #
#                                      #
########################################

if __name__ == "__main__":
    schema = InsightsGetRequestSchema()

    # Serialization
    expected = InsightsGetRequest(user_id=252342, history_window="1m")
    print(json.dumps(schema.dump(expected)))

    # Deserialization
    json_data = json.dumps(
        # Copy JSON from above print
        {"user_id": 252342, "history_window": "1m"}
    )
    result = schema.loads(json_data)
    
    # Validation
    assert(expected.user_id == result.user_id)
    assert(expected.history_window == result.history_window)
