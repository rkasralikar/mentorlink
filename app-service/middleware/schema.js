
module.exports = {
  TwoStepAuthentication : {
    
      "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "TwoStepVerfication",
      "type": "object",
      "properties": {
        "email": {
          "type": "string"
        },
        "phone": {
          "type": "string",
          "minimum": 0
        }
       
      }
     
    
  },

  SocialMediaRegistration : {
    "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "SocialMediaRegistration",
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "email": {
          "type": "string",
          "minimum": 0
        },
        "image": {
          "type": "string"
        },
        " sign_in_method": {
          "type": "string"
        },
        "skills": {
          "type": "array"
        },
        "interests": {
          "type": "array"
        },
        "career_summary": {
          "type": "string"
        },
        "location": {
          "type": "array"
        },
       
        

       
      },

      
     
  },

  UpdateRegisteredUser : {
    "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "UpdateRegisteredUser",
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "email": {
          "type": "string",
          "minimum": 0
        },
        "image": {
          "type": "string"
        },
        " sign_in_method": {
          "type": "string"
        },
        "skills": {
          "type": "array"
        },
        "interests": {
          "type": "array"
        },
        "career_summary": {
          "type": "string"
        },
        "location": {
          "type": "array"
        },
       
        

       
      },

      
     
  },

  PhoneRegistration : {
    "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "PhoneRegistration",
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "phone": {
          "type": "string",
          "minimum": 0
        },
        "image": {
          "type": "string"
        },
        " sign_in_method": {
          "type": "string"
        },
        "skills": {
          "type": "array"
        },
        "interests": {
          "type": "array"
        },
        "career_summary": {
          "type": "string"
        },
        "location": {
          "type": "array"
        },
       
        

       
      },
    
  
     
  },
  SendOtp : {
    
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "SendOtp",
    "type": "object",
    "properties": {
     
      "phone": {
        "type": "string",
        "minimum": 0
      }
     
    }
   
  
},

FeedSchema : {
    
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "FeedSchema",
  "type": "object",
  "properties": {
   
    "id": {
      "type": "double",
      
    }
   
  }
 

},
getUserProfile : {
  "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "getUserProfile",
      "type": "array",
      "items":{
      "type":"object",
      "properties": {
        
        "user_id": {
          "type": "number"
        },
        "profile_data":{
          "type":"object",
          "properties":{
          "name": {
            "type": "string",
           
          },
          "email": {
            "type": "string"
          },
          " phone": {
              "type": "string"
            },
            "linkedin_profile": {
              "type": "string"
            },
            "sign_in_method": {
              "type": "string"
            },
            "about": {
              "type": "string"
            },
            "total_exp": {
              "type": "string"
            },
            "interest": {
              "type": "array"
            },
            "skills": {
              "type": "array"
            },
            "saved_items": {
              "type": "array"
            },
       
          
          },
          "required": ["name","email","phone","linkedin_profile","sign_in_method","about","total_exp","interest","skills","saved_items"]
      }
       
       
},
"required": ["profile_data","user_id"]

}

}
}

