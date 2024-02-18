from marshmallow import Schema, fields, post_load
import json

########################################
#                                      #
#             Schema Class             #
#                                      #
########################################

class SampleGetRequestSchema(Schema):
    type = fields.Str()
    field1 = fields.Str()
    field2 = fields.Str()
    
    @post_load
    def create(self, data, **kwargs):
        return SampleGetRequest(**data)

########################################
#                                      #
#             Model  Class             #
#                                      #
########################################

class SampleGetRequest:
    def __init__(self, type, field1, field2):
        self.type = type
        self.field1 = field1
        self.field2 = field2

########################################
#                                      #
#              Validator               #
#                                      #
########################################

if __name__ == "__main__":
    schema = SampleGetRequestSchema()

    # Serialization
    expected = SampleGetRequest(type="I am a sample Request", field1="abcdef", field2="ghijkl")
    print(json.dumps(schema.dump(expected)))

    # Deserialization
    json_data = json.dumps(
        # Copy JSON from above print
        {"field2": "ghijkl", "field1": "abcdef", "type": "I am a sample Request"}
    )
    result = schema.loads(json_data)
    
    # Validation
    assert(expected.type == result.type)
    assert(expected.field1 == result.field1)
    assert(expected.field2 == result.field2)