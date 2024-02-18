const express = require("express");
const commentService = require("../service/commentService");
const commentActivityService = require("../service/commentActivityService");
const {SUCCESS} = require("../../../local/en/message");
const router = express.Router();

router.post("/", auth.check, (req,res,next) => {
    /*
         #swagger.path = '/feeds/comments'
         #swagger.tags = ['Comment']
         #swagger.description = 'Add comment on users post'
         #swagger.parameters['x-access-token'] = {
                  in: 'header',
                  required: true,
                  name:"x-access-token",
          }
         security: [ { x-access-token: [] } ],
         #swagger.parameters['Comment'] = {
                     in: 'body',
                     required: true,
                     description: "Add comment on users post",
                     schema: {
                      comment:"",
                      parent_id:"",
                      item_id:""
                                        
                    }
          }
         #swagger.responses[200] ={}
    */
    return commentService.add(req, res, next);
   });

router.get("/", auth.check, (req,res,next) => {
    /*
         #swagger.path = '/feeds/comments'
         #swagger.tags = ['Comment']
         #swagger.description = 'get all comments on feed by its item id'
         #swagger.parameters['x-access-token'] = {
                  in: 'header',
                  required: true,
                  name:"x-access-token",
          }
         security: [ { x-access-token: [] } ],
           #swagger.parameters['feed'] = {
                     in: 'query',
                     description: "get all comments on feed by its item id",
                     name: 'feed'
          }
         #swagger.responses[200] ={}
    */
     return commentService.getComment(req, res, next);
   });

router.get("/:id", auth.check, (req,res,next) => {
    /*
         #swagger.path = '/feeds/comments/{id}'
         #swagger.tags = ['Comment']
         #swagger.description = 'get all reply on comment by comment id'
         #swagger.parameters['x-access-token'] = {
                  in: 'header',
                  required: true,
                  name:"x-access-token",
          }
         security: [ { x-access-token: [] } ],

         #swagger.responses[200] ={}
    */
     return commentService.getCommentById(req, res, next);
   });

router.put("/:id", auth.check, (req, res, next) => {
/*
     #swagger.path = '/feeds/comments/{id}'
     #swagger.tags = ['Comment Activity']
     #swagger.description = "update likes and dislikes of comment"
     #swagger.parameters['x-access-token'] = {
             in: 'header',
             required: true,
             name:"x-access-token",
          }
     security: [ { x-access-token: [] } ],
     #swagger.parameters['CommentActivity'] = {
             in: 'body',
             required: true,
             description: 'update likes and dislikes of comment',
             schema: { 
                  dislike :false,
                  like    : false,
                  
               }
          }
     #swagger.responses[200] ={}
*/
 return commentActivityService.updatecomment(req, res, next);
})   
module.exports = router;
