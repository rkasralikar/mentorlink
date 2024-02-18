from marshmallow import Schema, fields, post_load
import json

########################################
#                                      #
#             Schema Class             #
#                                      #
########################################

class SampleGetResponseSchema(Schema):
    type = fields.Str()
    field1 = fields.Str()
    field2 = fields.Str()
    
    @post_load
    def create(self, data, **kwargs):
        return SampleGetResponse(**data)

########################################
#                                      #
#             Model  Class             #
#                                      #
########################################

class SampleGetResponse:
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
    schema = SampleGetResponseSchema()

    # Serialization
    expected = SampleGetResponse(type="I am a sample Response", field1="1234567", field2="910111213")
    print(json.dumps(schema.dump(expected)))

    # Deserialization
    json_data = json.dumps(
        # Copy JSON from above print
        {"field2": "910111213", "field1": "1234567", "type": "I am a sample Response"}
    )
    result = schema.loads(json_data)
    
    # Validation
    assert(expected.type == result.type)
    assert(expected.field1 == result.field1)
    assert(expected.field2 == result.field2)