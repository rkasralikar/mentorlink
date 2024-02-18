from marshmallow import Schema, fields, post_load
import json

########################################
#                                      #
#             Schema Class             #
#                                      #
########################################

class AnalyticsGetRequestSchema(Schema):
    type = fields.Str()
    entity = fields.Str()
    keys = fields.List(fields.Str())
    reduce = fields.Str()
    start_time = fields.Str()
    end_time = fields.Str()
    
    @post_load
    def create(self, data, **kwargs):
        return AnalyticsGetRequest(**data)

########################################
#                                      #
#             Model  Class             #
#                                      #
########################################

class AnalyticsGetRequest:
    def __init__(self, type: str, entity: str, keys: list[str], reduce: str, start_time: str, end_time: str):
        self.type = type
        self.entity = entity
        self.keys = keys
        self.reduce = reduce
        self.start_time = start_time
        self.end_time = end_time

########################################
#                                      #
#              Validator               #
#                                      #
########################################

if __name__ == "__main__":
    schema = AnalyticsGetRequestSchema()

    # Serialization
    expected = AnalyticsGetRequest(type="USER", entity="0252342", keys=["pages.visited"], reduce="top(10)", start_time="2020-01-01", end_time="now")
    print(json.dumps(schema.dump(expected)))

    # Deserialization
    json_data = json.dumps(
        # Copy JSON from above print
        {"entity": "0252342", "end_time": "now", "keys": ["pages.visited"], "reduce": "top(10)", "start_time": "2020-01-01", "type": "USER"}
    )
    result = schema.loads(json_data)
    
    # Validation
    assert(expected.type == result.type)
    assert(expected.entity == result.entity)
    assert(expected.keys == result.keys)
    assert(expected.reduce == result.reduce)
    assert(expected.start_time == result.start_time)
    assert(expected.end_time == result.end_time)
