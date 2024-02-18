
Validator.prototype._suppliedWithData = function(attribute) {
    return _.has(this.input, attribute);
};
Validator.register(
    'integer',
    function(value, requirement, attribute) {
        return _.isInteger(value);
    },
    'The :attribute must be an integer.'
);
Validator.register(
    'IsValidObjectID',
    function(value, requirement, attribute) {
        return ObjectId.isValid(value);
    },
    'The :attribute id is not valid.'
);
