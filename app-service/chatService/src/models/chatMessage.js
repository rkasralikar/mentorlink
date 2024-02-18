const Schema = Mongoose.Schema;


const { v4 } = require("uuid");
const uuidv4 = v4;
const MESSAGE_TYPES = {
    TYPE_TEXT: "text",
};
const readByRecipientSchema = Mongoose.Schema({
    _id: false,
    readByUserId: String,
    readAt: {
        type: Date,
        default: Date.now(),
    },
}, {
    timestamps: false,
});
const chatMessageSchema = Mongoose.Schema({
    
    chatRoomId:  { type: Schema.Types.ObjectId },
    chatUserId:{type:Schema.Types.ObjectId},
    message: Mongoose.Schema.Types.Mixed,
    type: {
        type: String,
       
    },
    textId:{type:Number,default:0},
    postedByUser:  { type: Schema.Types.ObjectId },
    readByRecipients: [readByRecipientSchema],
}, {
    timestamps: true,
    collection: "chatmessages",
});
/**
 * This method will create a post in chat
 *
 * @param {String} roomId - id of chat room
 * @param {Object} message - message you want to post in the chat room
 * @param {String} postedByUser - user who is posting the message
 */
chatMessageSchema.statics.createPostInChatRoom = async function(chatMessageBody) {
    console.log("body--->>",chatMessageBody)
    const {
        chatRoomId,
        message,
        postedByUser,
      //  readByRecipients: { readByUserId: postedByUser }
    } = chatMessageBody
    try {
        const post = await this.create({
            chatRoomId: chatRoomId,
            message: message,
            postedByUser: postedByUser,
          //  readByRecipients: readByRecipients: { readByUserId: postedByUser }
        });
      
        return post
    } catch (error) {
        throw error;
    }
}
/**
 * @param {String} chatRoomId - chat room id
 */
chatMessageSchema.statics.getConversationByRoomId = async function(chatRoomId, options = {}) {
    try {
        return this.aggregate([
            { $match: { chatRoomId } },
            { $sort: { createdAt: -1 } },
            // do a join on another table called users, and
            // get me a user whose _id = postedByUser
            {
                $lookup: {
                    from: 'users',
                    localField: 'postedByUser',
                    foreignField: '_id',
                    as: 'postedByUser',
                }
                },
            { $unwind: "$postedByUser" },
            // apply pagination
            { $skip: options.page * options.limit },
            { $limit: options.limit },
            { $sort: { createdAt: 1 } },
        ]);
    } catch (error) {
        throw error;
    }
}
/**
 * @param {String} chatRoomId - chat room id
 * @param {String} currentUserOnlineId - user id
 */
chatMessageSchema.statics.markMessageRead = async function(chatRoomId, currentUserOnlineId) {
    try {
        return this.updateMany({
            chatRoomId,
            'readByRecipients.readByUserId': { $ne: currentUserOnlineId }
            }, {
            $addToSet: {
                readByRecipients: { readByUserId: currentUserOnlineId }
            }
            }, {
            multi: true
        });
    } catch (error) {
        throw error;
    }
}
/**
 * @param {Array} chatRoomIds - chat room ids
 * @param {{ page, limit }} options - pagination options
 * @param {String} currentUserOnlineId - user id
 */
chatMessageSchema.statics.getRecentConversation = async function(chatRoomIds, options, currentUserOnlineId) {
    try {
        return this.aggregate([
            { $match: { chatRoomId: { $in: chatRoomIds } } },
            {
                $group: {
                    _id: '$chatRoomId',
                    messageId: { $last: '$_id' },
                    chatRoomId: { $last: '$chatRoomId' },
                    message: { $last: '$message' },
                    type: { $last: '$type' },
                    postedByUser: { $last: '$postedByUser' },
                    createdAt: { $last: '$createdAt' },
                    readByRecipients: { $last: '$readByRecipients' },
                }
                },
            { $sort: { createdAt: -1 } },
            // do a join on another table called users, and
            // get me a user whose _id = postedByUser
            {
                $lookup: {
                    from: 'users',
                    localField: 'postedByUser',
                    foreignField: '_id',
                    as: 'postedByUser',
                }
                },
            { $unwind: "$postedByUser" },
            // do a join on another table called chatrooms, and
            // get me room details
            {
                $lookup: {
                    from: 'chatrooms',
                    localField: '_id',
                    foreignField: '_id',
                    as: 'roomInfo',
                }
                },
            { $unwind: "$roomInfo" },
            { $unwind: "$roomInfo.userIds" },
            // do a join on another table called users
            {
                $lookup: {
                    from: 'users',
                    localField: 'roomInfo.userIds',
                    foreignField: '_id',
                    as: 'roomInfo.userProfile',
                }
                },
            { $unwind: "$readByRecipients" },
            // do a join on another table called users
            {
                $lookup: {
                    from: 'users',
                    localField: 'readByRecipients.readByUserId',
                    foreignField: '_id',
                    as: 'readByRecipients.readByUser',
                }
                },
            {
                $group: {
                    _id: '$roomInfo._id',
                    messageId: { $last: '$messageId' },
                    chatRoomId: { $last: '$chatRoomId' },
                    message: { $last: '$message' },
                    type: { $last: '$type' },
                    postedByUser: { $last: '$postedByUser' },
                    readByRecipients: { $addToSet: '$readByRecipients' },
                    roomInfo: { $addToSet: '$roomInfo.userProfile' },
                    createdAt: { $last: '$createdAt' },
                },
            },
            // apply pagination
            { $skip: options.page * options.limit },
            { $limit: options.limit },
        ]);
    } catch (error) {
        throw error;
    }
}
module.exports =  Mongoose.model("ChatMessage", chatMessageSchema);
