from marshmallow import Schema, fields, post_load
import json

########################################
#                                      #
#             Schema Class             #
#                                      #
########################################

class AnalyticsGetResponseSchema(Schema):
    type = fields.Str()
    entity = fields.Str()
    data = fields.Dict(keys=fields.Str(), values=fields.Int())
    
    @post_load
    def create(self, data, **kwargs):
        return AnalyticsGetResponse(**data)


########################################
#                                      #
#             Model  Class             #
#                                      #
########################################

class AnalyticsGetResponse:
    def __init__(self, type: str, entity: str, data: dict[str, int]):
        self.type = type
        self.entity = entity
        self.data = data

########################################
#                                      #
#              Validator               #
#                                      #
########################################

if __name__ == "__main__":
    schema = AnalyticsGetResponseSchema()

    # Serialization
    expected = AnalyticsGetResponse(type="USER", entity="0252342", data={"pages.visited.avg": 11, "pictures.shared.avg": 27})
    print(json.dumps(schema.dump(expected)))

    # Deserialization
    json_data = json.dumps(
        # Copy JSON from above print
        {"entity": "0252342", "type": "USER", "data": {"pages.visited.avg": 11, "pictures.shared.avg": 27}}
    )
    result = schema.loads(json_data)
    
    # Validation
    assert(expected.type == result.type)
    assert(expected.entity == result.entity)
    for key in expected.data.keys():
        assert(expected.data[key] == result.data[key])
