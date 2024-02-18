const express = require("express");
const router = express.Router();
const chatService = require("../service/chatService");

console.log("here in chat cont111");

router.post("/initiate", (req, res, next) => {
  /*
    #swagger.path = '/chats/initiate'
    #swagger.tags = ['Chat']
   #swagger.description = 'create chat room'
  
    #swagger.parameters['Chat'] = {
                in: 'body',
                required: true,
                description: "initiate chat room.",
                schema: {
                   userIds:[],
                   type:'',
                   id:[]
   
                }
     }
    #swagger.responses[200] ={}
   */

  chatService.initiate(req, res, next);
});

router.post("/sharefeed", auth.check, (req, res, next) => {
  /*
    #swagger.path = '/chats/sharefeed'
    #swagger.tags = ['Chat']
   #swagger.description = 'sharefeed in chatroom'
  
    #swagger.parameters['x-access-token'] = {
              in: 'header',
              required: true,
              name:"x-access-token",
              
            
            
     }
     security: [ { x-access-token: [] } ],
    #swagger.parameters['Chat'] = {
                in: 'body',
                required: true,
                description: "sharefeed in chatroom.",
                schema: {
                   userIds:[{
                     userId:'',
                     id:'',
                     lastMessage:''
                   }],
                   type:'',
                   id:''
                 
                   
                }
     }
    #swagger.responses[200] ={}
   */

  chatService.shareFeedInChatRoom(req, res, next);
});

router.post("/message", (req, res, next) => {
  /*
    #swagger.path = '/chats/message'
    #swagger.tags = ['Chat']
   #swagger.description = 'user send message.'
  
    #swagger.parameters['Chat'] = {
                in: 'body',
                required: true,
                description: "send message.",
                schema: {
                   message:"",
                   chatRoomId:'',
                   postedByUser:''
                }
     }
    #swagger.responses[200] ={}
   */
  console.log("here in chat cont");

  chatService.postMessage(req, res, next);
});

router.post("/saveMessage", auth.check, (req, res, next) => {
  /*
    #swagger.path = '/chats/saveMessage'
    #swagger.tags = ['Chat']
   #swagger.parameters['x-access-token'] = {
            in: 'header',
            required: true,
            name:"x-access-token",
   }
   #swagger.description = 'user send message.'
  
    #swagger.parameters['Chat'] = {
                in: 'body',
                required: true,
                description: "send message.",
                schema: {
                   message:"",
                   chatRoomId:'',
                   postedByUser:'',
                   type:'',
                   chatUserId:''
                }
     }
    #swagger.responses[200] ={}
   */
  console.log("here in chat cont2");

  chatService.postMessage(req, res, next);
});

router.post("/getChatHistory", (req, res, next) => {
  /*
    #swagger.path = '/chats/getChatHistory'
    #swagger.tags = ['Chat']
   #swagger.description = 'get chat history.'

   
    #swagger.parameters['Chat'] = {
                in: 'body',
                required: true,
                description: "get chat history.",
                schema: {
                 chatRoomId:'',
                 user:''
                }
     }
    #swagger.responses[200] ={}
   */
  console.log("here in chat cont2");

  chatService.getChatHistory(req, res, next);
});

router.get("/getMyChats",auth.check, (req,res,next)=>{
   /*
    #swagger.path = '/chats/getMyChats'
    #swagger.tags = ['Chat']
    #swagger.parameters['x-access-token'] = {
              in: 'header',
              required: true,
              name:"x-access-token",
     }
   #swagger.description = 'get users previous chat list.'
  

   */

  return chatService.getMyChats(req, res, next);
 
})

router.post('/getRecentUpdates', auth.check, (req, res, next) => {
 
  /*
    #swagger.path = '/chats/getRecentUpdates'
    #swagger.tags = ['Chat']
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
                description: "get recent updated users list.",
                schema: {
                  
                }
     }
    #swagger.responses[200] ={}
   */
 return chatService.GetRecentUpdatedUsers(req, res, next);
 
});


router.post('/getuserchatanalytics',auth.check,(req,res,next)=>{
   /*
    #swagger.path = '/chats/getuserchatanalytics'
    #swagger.tags = ['Chat']
   #swagger.description = 'get user chat analytics .'
   #swagger.parameters['x-access-token'] = {
              in: 'header',
              required: true,
              name:"x-access-token",
              
            
            
     }
     security: [ { x-access-token: [] } ],
    #swagger.parameters['User'] = {
                in: 'body',
                required: true,
                description: "get user chat analytics",
                schema: {
                 pageNo:'',
                 recordsPerPage:''
                }
     }
    #swagger.responses[200] ={}
   */

  return chatService.GetChatAnalytics(req, res, next);
})

router.post('/deleteRoomById', auth.check, (req, res, next) => {
 
  /*
    #swagger.path = '/chats/deleteRoomById'
    #swagger.tags = ['Chat']
   #swagger.description = 'Delete Room By Room Id.'
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
                schema: {_id:''}
     }
    #swagger.responses[200] ={}
   */
 return chatService.deleteRoomById(req, res, next);
 
});



module.exports = router;
