from marshmallow import Schema, fields, post_load
import json

########################################
#                                      #
#             Schema Class             #
#                                      #
########################################

class NudgesStatsSchema(Schema):
    interest = fields.Str()
    n_read = fields.Int()
    n_liked = fields.Int()
    n_saved = fields.Int()
    n_shared = fields.Int()

    @post_load
    def create(self, data, **kwargs):
        return NudgesStats(**data)

class InsightsGetResponseSchema(Schema):
    user_id = fields.Int()
    history_window = fields.Str()
    user_insights = fields.List(fields.Nested(NudgesStatsSchema))
    
    @post_load
    def create(self, data, **kwargs):
        return InsightsGetResponse(**data)

########################################
#                                      #
#             Model  Class             #
#                                      #
########################################

class NudgesStats:
    def __init__(self, interest: str, n_read: int, n_liked: int, n_saved: int, n_shared: int):
        self.interest = interest
        self.n_read = n_read
        self.n_liked = n_liked
        self.n_saved = n_saved
        self.n_shared = n_shared

class InsightsGetResponse:
    def __init__(self, user_id: int, history_window: str, user_insights: list[NudgesStats]):
        self.user_id = user_id
        self.history_window = history_window
        self.user_insights = user_insights

########################################
#                                      #
#              Validator               #
#                                      #
########################################

if __name__ == "__main__":
    schema = InsightsGetResponseSchema()

    # Serialization
    expected = InsightsGetResponse(user_id=252342, history_window="1m",
                                   user_insights=[NudgesStats(f"interest{cnt}", cnt, cnt, cnt, cnt) for cnt in range(3)])
    print(json.dumps(schema.dump(expected)))

    # Deserialization
    json_data = json.dumps(
        # Copy JSON from above print
        {"user_id": 252342, "history_window": "1m", "user_insights": [{"n_shared": 0, "interest": "interest0", "n_saved": 0, "n_read": 0, "n_liked": 0}, {"n_shared": 1, "interest": "interest1", "n_saved": 1, "n_read": 1, "n_liked": 1}, {"n_shared": 2, "interest": "interest2", "n_saved": 2, "n_read": 2, "n_liked": 2}]}
    )
    result = schema.loads(json_data)
    
    # Validation
    assert(expected.user_id == result.user_id)
    assert(expected.history_window == result.history_window)
    for eui,rui in zip(expected.user_insights, result.user_insights):
        assert(eui.interest == rui.interest)
        assert(eui.n_read == rui.n_read)
        assert(eui.n_liked == rui.n_liked)
        assert(eui.n_saved == rui.n_saved)
        assert(eui.n_shared == rui.n_shared)
