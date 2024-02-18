const express = require('express');
const router = express.Router();
const InterestService = require("../service/interestService")
router.get('/', (req, res, next)=> {
    /*
    #swagger.path = '/interests'
    #swagger.tags = ['Interest']
    #swagger.description = 'get list of interests.'
   */
    /* #swagger.responses[200] = {schema: {},
                    description: "" } */
    InterestService.GetInterests(req, res, next);
});

router.post('/', (req, res, next)=>{
    /*
       #swagger.path = '/interests'
      #swagger.tags = ['Interest']
      #swagger.description = 'save new interest.'
     #swagger.parameters['obj'] = {
                  in: 'body',
                  required: true,
                  description: "interest data.",
                  schema: {
                 name:''
                  },
       }
      #swagger.responses[200] ={}
     */
    InterestService.SaveInterest(req, res, next);
});



module.exports = router;
