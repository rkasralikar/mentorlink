const express = require('express');
const router = express.Router();
const UserService = require("../service/userService");


router.post('/register-with-social-media', Func.validate(Rules.SocialMediaRegistration), validator.schemaValidator(JSONSchema.SocialMediaRegistration), Analytics.event, (req, res, next) => {
    /*
        #swagger.path = '/users/register-with-social-media'
        #swagger.tags = ['User']
        #swagger.description = 'register user with social media'
       #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "register user",
                schema: {
                    userid: '',
                    name: '',
                    email: '',
                    image: '',
                    sign_in_method: '',
                    ssid:'',
                    skills: [ ],
                    interests: [ ],
                    career_summary: '',
                    location: ["lat","long"],
                    term_accepted: 1,
                    category: 'register',
                    action: 'for register',
                    label: 'Register user by phone.',
                    value: '1',
                    deviceId:'',
                    osVersion:'',
                    osType:'',
                    deviceName:'',
                    deviceToken:''
                  }
       }
        #swagger.responses[200] ={}
       */
    return UserService.SocialMediaRegister(req, res, next);
});

router.post('/update-user-information/', auth.check, validator.schemaValidator(JSONSchema.UpdateRegisteredUser), (req, res, next) => {
    /*
        #swagger.path = '/users/update-user-information'
        #swagger.tags = ['User']
        #swagger.description = 'update registered user information'

         #swagger.parameters['x-access-token'] = {
              in: 'header',
                  required: true,
                  name:"x-access-token",
       }
       security: [ { x-access-token: [] } ],

        #swagger.parameters['User'] = {


                in: 'body',
                required: false,
                description: "update user information",
                schema: {
                    userid: '',
                    name: '',
                    email: '',
                    image: '',
                    sign_in_method: '',
                    skills: [ ],
                    interests: [ ],
                    career_summary: '',
                    location: ["lat","long"],
                    term_accepted: 1,
                    category: 'register',
                    action: 'for register',
                    label: 'Register user by phone.',
                    is_career_summary:'',
                    last_login_time:'',
                    value: '1'
               },


       }



        #swagger.responses[200] ={}
       */
    return UserService.UpdateRegisteredUser(req, res, next);
});

router.post('/register-with-phone', Func.validate(Rules.RegisterWithPhone), validator.schemaValidator(JSONSchema.PhoneRegistration), Analytics.event, (req, res, next) => {
    /*
        #swagger.path = '/users/register-with-phone'
        #swagger.tags = ['User']
        #swagger.description = 'register user'
        #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "register user",
                schema: {
                    name: '',
                    phone: '',
                    sign_in_method: '',
                    ssid:'',
                    skills: [ ],
                    interests: [ ],
                    career_summary: '',
                    location: ["lat","long"],
                    term_accepted: 1,
                    image: '',
                    category: 'register',
                    action: 'for register',
                    label: 'Register user by phone.',
                    value: '1',
                    deviceId:'',
                   osVersion:'',
                   osType:'',
                   deviceName:'',
                   deviceToken:''
                  }


       }

        #swagger.responses[200] ={}
       */
    return UserService.RegisterWithPhone(req, res, next);
});

router.post('/register-with-email', Func.validate(Rules.EmailRegistration), Analytics.event, (req, res, next) => {
    /*
        #swagger.path = '/users/register-with-email'
        #swagger.tags = ['User']
        #swagger.description = 'register user'
        #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "register user",
                schema: {
                    name: '',
                    email: '',
                    phone: '',
                    password: '',
                    linkedin_profile: '',
                    sign_in_method: '',
                    skills: [ ],
                    interests: [ ],
                    career_summary: '',
                    location: ["lat","long"],
                    term_accepted: 1,
                    image: '',
                    category: 'register',
                    action: 'for register',
                    label: 'Register user by phone.',
                    value: '1'
                  }
       }


        #swagger.responses[200] ={}
       */
    return UserService.Register(req, res, next);
});

router.get('/profile', auth.check, function (req, res, next) {
    /*

   #swagger.path = '/users/profile'
   #swagger.tags = ['User']
    #swagger.description = 'get user Information by Id'
    #swagger.parameters['x-access-token'] = {
                  in: 'header',
                  required: true,
                  name:"x-access-token",



         }
         security: [ { x-access-token: [] } ],
     #swagger.description = 'Endpoint to get user by id.'
  */
    /* #swagger.responses[200] = {}
     */
    return UserService.GetUsers(req, res, next);


});


router.post('/allprofiles', auth.check, function (req, res, next) {
    /*

  #swagger.path = '/users/allprofiles'
  #swagger.tags = ['User']
  #swagger.description = 'get all user profile Information with pagination'
              #swagger.parameters['x-access-token'] = {
              in: 'header',
                  required: true,
                  name:"x-access-token",



         }
         security: [ { x-access-token: [] } ],

    #swagger.parameters['User'] = {
                  in: 'body',
                  required: true,
                  description: "get all user information",
                  schema: {
                     pageNo : ' ',
                     recordsPerPage : ' '
                    }
         }

   #swagger.description = 'get all user profile Information with pagination.'
  */
    /* #swagger.responses[200] = {}
     */
    return UserService.GetAllUsers(req, res, next);
});


router.post('/two-step-authentication', auth.check, validator.schemaValidator(JSONSchema.TwoStepAuthentication), function (req, res, next) {

    /*
        #swagger.path = '/users/two-step-authentication'
        #swagger.tags = ['User']
        #swagger.description = 'register user'

         #swagger.parameters['x-access-token'] = {
                  in: 'header',
                  required: true,
                  name:"x-access-token",



         }
         security: [ { x-access-token: [] } ],
        #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "Two step authentication ",
                schema: {

                    email: '',
                    phone: ''

                  }
       }


        #swagger.responses[200] ={}
       */
    return UserService.TwoStepAuthentication(req, res, next);

});


router.get('/getUsersList', auth.check, function (req, res, next) {
    /*

  #swagger.path = '/users/getUsersList'
  #swagger.tags = ['User']
  #swagger.description = 'get all active users'
  #swagger.parameters['x-access-token'] = {
                in: 'header',
                required: true,
                name:"x-access-token",



       }
       security: [ { x-access-token: [] } ],
   #swagger.description = 'get all active users'
  */
    /* #swagger.responses[200] = {}
     */
    return UserService.GetActiveUsers(req, res, next);


});


router.post('/login', Func.validate(Rules.UserLogin), (req, res, next) => {

    /*
      #swagger.path = '/users/login'
      #swagger.tags = ['User']
     #swagger.description = 'validate user credentials.'
      #swagger.parameters['User'] = {
                  in: 'body',
                  required: true,
                  description: "User data.",
                  schema: {email:'',password:''}
       }
      #swagger.responses[200] ={}
     */
    return UserService.Login(req, res, next);

});

router.post('/getRecentUpdates', auth.check, (req, res, next) => {

    /*
      #swagger.path = '/users/getRecentUpdates'
      #swagger.tags = ['User']
     #swagger.description = 'get recent updated users list.'
     #swagger.parameters['x-access-token'] = {
                in: 'header',
                required: true,
                name:"x-access-token",
       }
       security: [ { x-access-token: [] } ],
      #swagger.parameters['User'] = {
                  in: 'body',
                  required: true,
                  description: "User data.",
                  schema: {datetime:''}
       }
      #swagger.responses[200] ={}
     */
    return UserService.GetRecentUpdatedUsers(req, res, next);

});

router.post('/sendotp', validator.schemaValidator(JSONSchema.SendOtp), (req, res, next) => {
    /*
        #swagger.path = '/users/sendotp'
        #swagger.tags = ['User']
        #swagger.description = 'send user signup otp'

           #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "send user signup otp ",
                schema: {

                    phone: ''

                  }
       }


        #swagger.responses[200] ={}
       */
    return UserService.sendOtp(req, res, next);

});


router.post('/verifyotp', (req, res, next) => {
    /*
        #swagger.path = '/users/verifyotp'
        #swagger.tags = ['User']
        #swagger.description = 'verify user signup otp'

           #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "verify user signup otp ",
                schema: {
                    email:'',
                    phone: '',
                    code:''

                  }
       }


        #swagger.responses[200] ={}
       */
    return UserService.verifyOtp(req, res, next);

});

router.get('/token', auth.check, (req, res, next) => {

    /*
      #swagger.path = '/users/token'
      #swagger.tags = ['User']
     #swagger.description = 'get recent updated users list.'
     #swagger.parameters['x-access-token'] = {
                in: 'header',
                required: true,
                name:"x-access-token",
       }
       security: [ { x-access-token: [] } ],
      #swagger.responses[200] ={}
     */
    return UserService.getToken(req, res, next);

});

router.post('/getShareFeedList', (req, res, next) => {
    /*
        #swagger.path = '/users/getShareFeedList'
        #swagger.tags = ['User']
        #swagger.description = 'get share feed user list'

           #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "get share feed user list ",
                schema: {
                    id:''


                  }
       }


        #swagger.responses[200] ={}
       */
    return UserService.getShareFeedUserList(req, res, next);
});

router.post('/generateRegistrationToken', (req, res, next) => {
    /*
        #swagger.path = '/users/generateRegistrationToken'
        #swagger.tags = ['User']
        #swagger.description = 'generate authentication token'


          #swagger.responses[200] ={}
       */
    return UserService.generateRegistrationToken(req, res, next);
});

router.post('/get-user-info', auth.check, (req, res, next) => {
    /*
            #swagger.path = '/users/get-user-info'
            #swagger.tags = ['User']
            #swagger.description = 'get user details based on mobile number or email'
            #swagger.parameters['x-access-token'] = {
                            in: 'header',
                            required: true,
                            name:"x-access-token",
                   }
            schema: {
                     contacts : [],
                     emails : []
                    }
              #swagger.responses[200] ={}
           */
    return UserService.getUserInfo(req, res, next);
})

router.post('/send-invite', auth.check, (req, res, next) => {
    /*
            #swagger.path = '/users/send-invite'
            #swagger.tags = ['User']
            #swagger.description = 'send invitation to user to join mentor-link app'
            #swagger.parameters['x-access-token'] = {
                            in: 'header',
                            required: true,
                            name:"x-access-token",
                   }
            #swagger.parameters['contacts'] = {
                        in: 'body',
                        required: true,
                        description: "list of users ",
                        schema: [{
                            name:'',
                            phone:'',
                            email:''
                          }]
               }
              #swagger.responses[200] ={}
           */
    return UserService.sendInvite(req, res, next);
})

module.exports = router;