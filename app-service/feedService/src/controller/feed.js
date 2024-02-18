const express = require('express');
const router = express.Router();
const FeedService = require("../service/feedService");
router.post('/', auth.check, (req, res, next) => {
    /*
    #swagger.path = '/feeds'
    #swagger.tags = ['Feed']
    #swagger.description = 'get list of feeds according to user interests',

     #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],

     #swagger.parameters['Feed'] = {
                in: 'body',
                required: true,
                description: "get list of feeds according to user interests",
                schema: {
                                 
                    interests: [],
                    category: 'register',
                    action: 'for register',
                    label: 'Register user by phone.',
                    value: '1'
                  }
       }
   */
    /* #swagger.responses[200] = schema: {}
      
                    */
    FeedService.GetFeeds(req, res, next);
});

router.post('/ids', auth.check, (req, res, next) => {
    /*
    #swagger.path = '/feeds/ids'
    #swagger.tags = ['Feed']
    #swagger.description = 'get list of feed ids according to user interests',

     #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],

     #swagger.parameters['Feed'] = {
                in: 'body',
                required: true,
                description: "get list of feed ids according to user interests",
                schema: {

                    interests: [],
                    category: 'register',
                    action: 'for register',
                    label: 'Register user by phone.',
                    value: '1'
                  }
       }
   */
    /* #swagger.responses[200] = schema: {}

                    */
    FeedService.GetFeedIds(req, res, next);
});

router.post('/data', auth.check, (req, res, next) => {
    /*
    #swagger.path = '/feeds/data'
    #swagger.tags = ['Feed']
    #swagger.description = 'get feed details according to feed ids',

     #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],

     #swagger.parameters['Feed'] = {
                in: 'body',
                required: true,
                description: "get feed details according to itemIds",
                schema: {
                    itemIds: [],
                  }
       }
   */
    /* #swagger.responses[200] = schema: {}

                    */
    FeedService.GetFeedData(req, res, next);
});


// router.post('/getFeeds', (req, res, next)=> {
//   /*
//   #swagger.path = '/feeds/getFeeds'
//   #swagger.tags = ['Feed']
//   #swagger.description = 'get list of feeds according to user interests',

//    #swagger.parameters['Feed'] = {
//               in: 'body',
//               required: true,
//               description: "get list of feeds according to user interests",
//               schema: {

//                   interests: [],
//                   category: 'register',
//                   action: 'for register',
//                   label: 'Register user by phone.',
//                   value: '1'
//                 }
//      }
//  */
//   /* #swagger.responses[200] = schema: {}

//                   */
//   FeedService.getAllFeeds(req, res, next);
// });


router.post('/update-like-information/:id', auth.check, validator.feedSchemaValidator(JSONSchema.FeedSchema), Analytics.event, (req, res, next) => {
    /*
        #swagger.path = '/feeds/update-like-information/{id}'

        #swagger.tags = ['Feed']
        #swagger.description = 'update feed information (like,unlike etc)'
       
         #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],
        #swagger.parameters['Feed'] = {
                in: 'body',
                required: false,
                description: "update feed information (like,unlike etc)",
                schema: {
                    liked:true,
                  }
        }
        #swagger.responses[200] ={}
       */
    return FeedService.UpdateLikeInformation(req, res, next);
});

router.post('/addDummmy', (req, res, next) => {
    /*
        #swagger.path = '/feeds/addDummmy'

        #swagger.tags = ['Feed']
        #swagger.description = 'update feed information (like,unlike etc)'
       
              
        #swagger.responses[200] ={}
       */
    return FeedService.addUserActivities(req, res, next);
});

router.post('/update-dislike-information/:id', auth.check, validator.feedSchemaValidator(JSONSchema.FeedSchema), Analytics.event, (req, res, next) => {
    /*
        #swagger.path = '/feeds/update-dislike-information/{id}'
        #swagger.tags = ['Feed']
        #swagger.description = 'update feed information (like,unlike etc)'
       
         #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],

        #swagger.parameters['Feed'] = {
                in: 'body',
                required: false,
                description: "update feed information (like,unlike etc)",
                schema: {
                    disliked:true,
                 }
       }

        #swagger.responses[200] ={},
      
       */
    return FeedService.UpdateDisLikeInformation(req, res, next);
});

router.post('/update-save-information/:id', auth.check, validator.feedSchemaValidator(JSONSchema.FeedSchema), Analytics.event, (req, res, next) => {
    /*
        #swagger.path = '/feeds/update-save-information/{id}'
        #swagger.tags = ['Feed']
        #swagger.description = 'update feed information (saved or unsaved etc)'
       
         #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],

        #swagger.parameters['Feed'] = {
                in: 'body',
                required: false,
                description: "update feed information (saved or unsaved etc)",
                schema: {
                    save_info:[{
                    isSaved:"",
                  

                    }]
                  }
        
                  
                 
                 
       }
       
                
              
        #swagger.responses[200] ={}
       */
    return FeedService.UpdateSaveInformation(req, res, next);
});


router.post('/savedfeeds', auth.check, (req, res, next) => {
    /*
    #swagger.path = '/feeds/savedFeeds'
    #swagger.tags = ['Feed']
    #swagger.description = 'get list of feeds saved by the user'

     #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],

     #swagger.parameters['Feed'] = {
                in: 'body',
                required: true,
                description: "get list of feeds saved by the user",
                schema: {
                                 
                 
                    category: 'register',
                    action: 'for register',
                    label: 'Register user by phone.',
                    value: '1'
                  }
       }
   */
    /* #swagger.responses[200] = schema: {}
      
                    */
    FeedService.GetSavedFeeds(req, res, next);
});

router.post('/update-visit-information/:id', auth.check, validator.feedSchemaValidator(JSONSchema.FeedSchema), Analytics.event, (req, res, next) => {
    /*
        #swagger.path = '/feeds/update-visit-information/{id}'

        #swagger.tags = ['Feed']
        #swagger.description = 'update feed information (like,unlike,visited etc)'

         #swagger.parameters['x-access-token'] = {
            in: 'header',
                required: true,
                name:"x-access-token",
     }
     security: [ { x-access-token: [] } ],


        #swagger.responses[200] ={}
       */
    return FeedService.visitFeed(req, res, next);
});


router.post('/alluseractivities', function (req, res, next) {
    /*

  #swagger.path = '/feeds/alluseractivities'
  #swagger.tags = ['Feed']
  #swagger.description = 'get all user activities Information with pagination'

   #swagger.parameters['x-access-token'] = {
              in: 'header',
                  required: true,
                  name:"x-access-token",



         }
         security: [ { x-access-token: [] } ],

    #swagger.parameters['Feed'] = {
                  in: 'body',
                  required: true,
                  description: "get all user activities",
                  schema: {
                     pageNo : ' ',
                     recordsPerPage : ' '
                    }
         }

   #swagger.description = 'get all user activities with pagination.'
  */
    /* #swagger.responses[200] = {}
                    */
    return FeedService.GetALLUserActivities(req, res, next);
});

router.post('/userprofileanalytics', auth.check, function (req, res, next) {
    /*

  #swagger.path = '/feeds/userprofileanalytics'
  #swagger.tags = ['Feed']
  #swagger.description = 'maintain user profile analytics information'

   #swagger.parameters['x-access-token'] = {
              in: 'header',
                  required: true,
                  name:"x-access-token",



         }
         security: [ { x-access-token: [] } ],

    #swagger.parameters['Feed'] = {
                  in: 'body',
                  required: true,
                  description: "maintain user profile analytics information",
                  schema: {
                   user_id:'',
                  numSavedFeed : ' ' ,
                 lastLoginTime : '',
                 numFeedVisited: '',
                 totalTimeSpent : '',
                 searchedKeywords : '',

                 appVersion : ''
                    }
         }

   #swagger.description = 'maintain user profile analytics information'
  */
    /* #swagger.responses[200] = {}
                    */

    return FeedService.userProfileAnalytics(req, res, next);
}),

    router.post('/getuserprofileanalytics', auth.check, function (req, res, next) {
        console.log("here in controller")
        /*

     #swagger.path = '/feeds/getuserprofileanalytics'
     #swagger.tags = ['Feed']
     #swagger.description = 'maintain user profile analytics information'

      #swagger.parameters['x-access-token'] = {
                 in: 'header',
                     required: true,
                     name:"x-access-token",



            }
            security: [ { x-access-token: [] } ],

            #swagger.parameters['Feed'] = {
                     in: 'body',
                     required: true,
                     description: "maintain user profile analytics information",
                     schema: {
                    pageNo : '',
                    pageSize : ''
                       }
            }

      #swagger.description = 'maintain user profile analytics information'
     */
        /* #swagger.responses[200] = {}
                        */


        return FeedService.GetUserProfileAnalytics(req, res, next);


    }),


    module.exports = router;
