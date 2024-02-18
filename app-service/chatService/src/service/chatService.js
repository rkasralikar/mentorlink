const initiate = async (req, res) => {
    try {
        const {userIds, type, id} = req.body;
        try {
            const dbChatRoom = await Models.ChatRoom.findOne(
                {
                    userIds: {
                        $size: userIds.length,
                        $all: [...userIds],
                    },
                });
            if (dbChatRoom) {
                Logger.logInfo(`Success in getting old room information for users: "${req.body.userIds}"`);
                return res.status(200).json({
                    message: "Successfully returned old room",
                    data: {
                        userIds: dbChatRoom.userIds,
                        type: dbChatRoom.type,
                        chatRoomId: dbChatRoom._id,
                        id: dbChatRoom.id
                    },
                });
            }
            const chatRoom = await new Models.ChatRoom({ userIds: userIds, type: type, id: id }).save();
            Logger.logInfo(`Success in getting new room information for users: "${req.body.userIds}"`);
            return res.status(200).json({
                message: "Successfully returned new room",
                data: {
                    userIds: chatRoom.userIds,
                    type: chatRoom.type,
                    id: chatRoom.id,
                    chatRoomId: chatRoom._id,
                },
            });
        } catch (error) {
            console.log(error);
            throw error;
        }
    } catch (error) {
        return res.status(500).json({success: false, error: error});
    }

};

const shareFeedInChatRoom = async (req, res) => {
  try {
        const {userIds, type, id} = req.body
        const {user} = req;
        const loginUserId = user.user;
        const cuid = parseInt(id)
        let roomIds = []
        for (const userId of userIds) {
            let ids = [loginUserId, userId.userId]
            let cuids = [cuid, parseInt(userId.id)]
            let lastMessage = userId.lastMessage
            let messageType = "text"
            const room = await createRoom(ids, type, cuids, lastMessage, messageType);
            if (room) {
                roomIds.push(room._id)
            }
        }
        return res.status(200).json({
            message: "Successfully returned old room",
            data: {
                userIds: userIds,
                type: type,
                roomIds: roomIds

            },
        });
    } catch (error) {
        Logger.error("error--->>", error)
        console.log("error creating room-->>", error);
        throw error;
    }


};

const createRoom = async (userIds, type, uids, lastMessage, messageType ) => {

    try {
        const room =   Models.ChatRoom.findOne({ userIds: { $size: userIds.length,  $all: [...userIds] }});
        if (room) {
            Logger.logInfo("chatroomObj-->>", room)
            return room;
        }
        return new Models.ChatRoom({
            userIds: userIds, type: type, id: uids, lastMessage: lastMessage,
            messageType: messageType
        }).save();

    }catch (error) {
        console.log(error);
        throw error;
    }


}
const postMessage = async (req, res, _next) => {
    try {
        const {chatRoomId, message, postedByUser, type} = req.body;
        const postmessage = new Models.ChatMessage({
            chatRoomId: chatRoomId,
            message: message,
            postedByUser: postedByUser,
            type: type,
        });
        await postmessage.save();
        const updateTime = Date.now();
        await Models.ChatRoom.findOneAndUpdate(
            {_id: ObjectId(chatRoomId)},
            {
                $set: {
                    updatedAt: updateTime,
                    lastMessage: message,
                    messageType: type,
                },
            }
        );
        getUserToken(chatRoomId, postedByUser, message)
        return res.send({
            message: "message sent successfully"
        })
    } catch (error) {
        Logger.error("error--->>", error)
        throw error;
    }
};


const getUserToken = async (chatRoomId, postedByUser, message) => {

    try {
        const data = await Models.ChatRoom.aggregate([
            {
                $match: {
                    _id: new ObjectId(chatRoomId)
                }
            },
            {
                $unwind: "$userIds",
            },
            {$match: {"userIds": {$ne: new ObjectId(postedByUser)}}},
            {
                $lookup: {
                    from: "users",
                    localField: "userIds",
                    foreignField: "_id",
                    as: "users",
                },
            },

            {
                $unwind: "$users",
            },


            {
                $group: {

                    "_id": "$users._id",
                    deviceToken: {$first: "$users.device_data.deviceToken"}
                }
            },

            {
                $project: {
                    _id: 0,
                    deviceToken: 1


                },
            },
        ]);
        if (data && data.length > 0) {
            let tokens = data[0].deviceToken
            tokens.forEach(token => {
                if (token != null) {
                    if (token.trim().length > 0) {
                        sendNotification(token, message)
                    }
                }

            })
        } else {
            Logger.logInfo("User tokens are missing --->>", chatRoomId);
        }

    }catch (e) {
        console.log(" getUserToken ", e);
        //throw  e;
    }
}

const sendNotification = function (registrationToken, message) {
    Logger.logInfo("registrationToken--->>", registrationToken)
    const payload = {
        notification: {
            title: "Chat Message",
            body: message
        },
    };
    admin.messaging().sendToDevice(registrationToken, payload)
        .then(response => {
            Logger.logInfo("response--->>", response)
        })
        .catch(error => {
            Logger.error(error);
            throw error;
        });

};


const getChatHistory = async (req, res, _next) => {
    const chatRoomId = req.body.chatRoomId;
    try {
        const chatHistory = await Models.ChatMessage.find(
            {
                chatRoomId: new ObjectId(chatRoomId)
            },
        ).sort({createdAt: -1})
        Logger.logInfo("chatHistory--->>", chatHistory);
        if (chatHistory) {
            return res.json({
                message: "Success",
                data: chatHistory
            });
        } else if (!chatHistory) {
            res.json({
                message: "Data not found"
            })
        }

    } catch (error) {
        console.log(error);
        throw error;
    }
}

const getAllUserRooms = async (data) => {
    const chatRoomId = data.chatRoomId;
    try {
        return await Models.ChatRoom.findOne(
            {
                _id: new ObjectId(chatRoomId)
            },
            {_id: 1}
        );
    } catch (error) {
        console.log(error);
        throw error;
    }
};
const getRecentConversation = async (req, res) => {
    const {user} = req;
    try {
        const currentLoggedUser = user.user;
        const options = {
            page: parseInt(req.query.page) || 0,
            limit: parseInt(req.query.limit) || 10,
        };
        const rooms = await ChatRoomModel.getChatRoomsByUserId(currentLoggedUser);
        const roomIds = rooms.map((room) => room._id);
        const recentConversation = await ChatMessageModel.getRecentConversation(
            roomIds,
            options,
            currentLoggedUser
        );
        return res
            .status(200)
            .json({success: true, conversation: recentConversation});
    } catch (error) {
        return res.status(500).json({success: false, error: error});
    }
};

const markConversationReadByRoomId = async (req, res) => {
    const {user} = req;
    try {
        const {roomId} = req.params;
        const room = await ChatRoomModel.getChatRoomByRoomId(roomId);
        if (!room) {
            return res.status(400).json({
                success: false,
                message: "No room exists for this id",
            });
        }

        const currentLoggedUser = user.user;
        const data = await ChatMessageModel.markMessageRead(
            roomId,
            currentLoggedUser
        );
        return res.status(200).json({success: true, data});
    } catch (error) {
        console.log(error);
        return res.status(500).json({success: false, error});
    }
};

const deleteRoomById = async (req, res, next) => {
    try {
        Logger.logInfo("roomId--->>", req.body._id);
        Models.ChatRoom.deleteOne(
            {_id: ObjectId(req.body._id)},

            (err, roomData) => {
                if (err) {
                    Logger.error("Update user err: ", err);
                    return next(setError(MSG.INTERNAL_ERROR, 500));
                } else if (roomData.length == 0) {
                    return next(setError(MSG.DATA_NOT_FOUND));
                } else {
                    return res.send({data: roomData, message: MSG.SUCCESS});
                }
            }
        );
    } catch (error) {
        return res.status(500).json({success: false, error: error});
    }
};
const deleteMessageById = async (req, res) => {
    try {
        const {messageId} = req.params;
        const message = await ChatMessageModel.remove({_id: messageId});
        return res.status(200).json({
            success: true,
            deletedMessagesCount: message.deletedCount,
        });
    } catch (error) {
        return res.status(500).json({success: false, error: error});
    }
};

const getMyChats = async (req, res) => {
    const {user} = req;
    const userId = new ObjectId(user.user);
    Models.ChatRoom.aggregate([

        {
            $match: {
                userIds: userId,
                lastMessage: {$ne: ""}
            },
        },
        {
            $unwind: "$userIds",
        },
        {$match: {"userIds": {$ne: new ObjectId(userId)}}},
        {
            $lookup: {
                from: "users",
                localField: "userIds",
                foreignField: "_id",
                as: "users",
            },
        },

        {
            $unwind: "$users",
        },
        {$sort: {updatedAt: -1}},

        {
            $project: {
                _id: 1,
                type: 1,
                lastMessage: 1,
                messageType: 1,
                updatedAt: 1,

                users: {
                    _id: 1,
                    name: 1,
                    image: 1,

                },
            },
        },
    ]).exec(function (err, data) {
        if (err) {
            Logger.error(`Error in getting my chat information for user: "${userId}"`);
            console.log("error--->>", err);
            throw err;
        } else {
            Logger.logInfo(`Success in getting my chat information for user: "${userId}"`);
            return res.status(200).json({
                data: data,
            });
        }
    });
};


const GetRecentUpdatedUsers = async (req, res) => {
    const {user} = req;
    const userId = new ObjectId(user.user);
    let currentTime = new Date();
    Logger.logInfo("currentDate-->>", currentTime);
    let matchCondition = {
        $and: [
            {"users._id": {$ne: userId}},
            {"users.is_career_summary": "1"},
            {"users.update24hrsTime": {$gt: currentTime}},
        ],
    };

    try {
        const userList = await Models.ChatRoom.aggregate([
            {
                $match: {
                    userIds: userId,
                },
            },
            {
                $unwind: "$userIds",
            },
            {
                $lookup: {
                    from: "users",
                    localField: "userIds",
                    foreignField: "_id",
                    as: "users",
                },
            },

            {
                $unwind: "$users",
            },
            {
                $match: matchCondition,
            },

            {$sort: {updatedAt: -1}},

            {
                $project: {
                    _id: 0,
                    users: {
                        _id: 1,
                        name: 1,
                        image: 1,
                        career_summary: 1,
                        updatedAt: 1
                    },
                },
            },
        ]);
        return res.status(200).json({
            data: userList,
            currentDateTime: new Date(),
        });
    }catch (e) {
        console.err(e);
        throw e;
    }
};


const GetChatAnalytics = function (req, res, next) {

    let recordsNo = parseInt(req.body.recordsPerPage);
    let pageNo = parseInt(req.body.pageNo);
    let start = recordsNo * (pageNo - 1);
    let limit = recordsNo;

    Models.ChatRoom.aggregate([

        {$skip: start},
        {$limit: limit},
        {
            $project: {
                _id: 0,
                user_id: "$chat_initiator",
                "chat_info": {
                    peer_list: "$id",
                    group_list: ["$groupNumber"],

                }
            }
        }


    ]).exec(function (err, chatAnalytics) {
        if (err) {
            Logger.error(`Error in getting my chat analytics for users`);
            console.log("error-->>", err);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        } else if (!chatAnalytics) {
            return next(setError(MSG.DATA_NOT_FOUND));
        } else {
            Logger.logInfo(`success in getting my chat analytics for users`);
            return res.send({data: chatAnalytics, message: MSG.DATA_FOUND});
        }
    })
}


module.exports = {
    initiate,
    postMessage,
    deleteMessageById,
    deleteRoomById,
    markConversationReadByRoomId,
    getRecentConversation,
    getAllUserRooms,
    getMyChats,
    GetRecentUpdatedUsers,
    GetChatAnalytics,
    shareFeedInChatRoom,
    getChatHistory

};
