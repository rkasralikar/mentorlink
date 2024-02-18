var Validator = require("jsonschema").Validator;
var v = new Validator();

module.exports = {
  schemaValidator: function (schema) {
    return function (req, res, next) {
      console.log("schema--->>>", schema);
      object = req.body;
      const validatedResponse = v.validate(object, schema);
      console.log("validatedResponse--->>>", validatedResponse);
      if(validatedResponse.errors.length >0 ){
        validatedResponse.errors.forEach(error => 
          {
            res.json({message:error.stack});
          }
          );

      } else{
        return next();
      }
     
    };

  },

  feedSchemaValidator: function (schema) {
    return function (req, res, next) {
      console.log("schema--->>>", schema);
      object = req.params;
      const validatedResponse = v.validate(object, schema);
      console.log("validatedResponse--->>>", validatedResponse);
      if(validatedResponse.errors.length >0 ){
        validatedResponse.errors.forEach(error => 
          {
            res.json({message:error.stack});
          }
          );

      } else{
        return next();
      }
      
    };

  },

      
};  
