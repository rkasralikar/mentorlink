const analytics = require("../../../middleware/analytics");
const axios = require("axios");
const async = require("async");
const {FeedServer} = Config;
const GetFeeds = async (req, res, next) => {
    const {user} = req;
    const interestList = req.body.interests
    const user_id = user.id;
    console.log("user_id-->>", typeof (user_id));
    if (!user_id) {
        return next(setError("User id is missing", 401));
    }
    async.waterfall([
            function getItemIds(callback) {
                let date = new Date();
                let url = FeedServer.feed_by_user + `%7B"user_id":${user_id},"interest_list":["${interestList}"]%7D`;
                Logger.logInfo(url,{});
                axios.get(url)
                    .then((response) => {
                        Logger.logInfo("data for id-->>" + response,{});
                        Logger.logInfo({"feed_referance_ids_time": new Date()-date},{});
                        const {data} = response
                        const items = data.item_id_info.slice(0, 90)
                        callback(null, items);
                    }).catch((err) => {
                    console.log("error-->>", err);
                    callback(err);
                });

            },
            function getFeedAnalytics(itemIds, callback) {
                getFeedMetaData(user_id).then(itemData => {
                    callback(null, itemIds, itemData)
                }).catch(err => {
                    console.log(err);
                    callback(err);
                })
            }
        ],
        function (err, itemIds, itemData) {
            if (err) {
                return next(setError(MSG.INTERNAL_ERROR, 500));
            }

            getItemInfos(itemIds, itemData, res, next);
        })
};

const GetFeedIds = async (req, res, next) => {
    const {user} = req;
    const interestList = req.body.interests
    const user_id = user.id;
    console.log("user_id-->>", typeof (user_id));
    if (!user_id) {
        return next(setError("User id is missing", 401));
    }
    async.waterfall([
            function getItemIds(callback) {
                let url = FeedServer.feed_by_user + `%7B"user_id":${user_id},"interest_list":["${interestList}"]%7D`;
                Logger.logInfo(url,{});
                axios.get(url)
                    .then((response) => {
                        console.log("data for id-->>", response)
                        const {data} = response
                        const items = data.item_id_info
                        callback(null, items);
                    }).catch((err) => {
                    console.log("error-->>", err);
                    callback(err);
                });

            }
        ],
        function (err, itemIds) {
            if (err) {
                return next(setError(MSG.INTERNAL_ERROR, 500));
            }
            return res.send({data: itemIds, message: MSG.DATA_FOUND});
        })
};

const GetFeedData = async (req, res, next) => {
    const {user} = req;
    const itemIds = req.body.itemIds
    const user_id = user.id;
    console.log("user_id-->>", typeof (user_id));
    if (!user_id) {
        return next(setError("User id is missing", 401));
    }
    async.waterfall([
            function getFeedAnalytics(callback) {
                getFeedMetaData(user_id).then(itemData => {
                    callback(null, itemIds, itemData)
                }).catch(err => {
                    callback(err);
                })
            }
        ],
        function (err, itemIds, itemData) {
            if (err) {
                return next(setError(MSG.INTERNAL_ERROR, 500));
            }
            getItemInfos(itemIds, itemData, res, next);
        })
};

const getFeedMetaData = (user_id) => {
    console.log("user id in feed meta data")
    return new Promise((resolve, reject) => {
        Models.UserActivity.aggregate([
            { $unwind: { path: "$activity", preserveNullAndEmptyArrays: true } },
            {
                $lookup: {
                    from: "comments",
                    let: {
                        item_id: "$activity.item_id"
                    },
                    pipeline: [{
                        $match: {
                            $expr: { $eq: ["$item_id", "$$item_id"] }
                        }
                    },
                    {
                        $count: "commentCount"
                    }],
                    as: "comment"
                }
            },
            { $unwind: { path: "$comment", preserveNullAndEmptyArrays: true } },
            {
                $group: {
                    _id: "$activity.item_id",
                    is_saved_feed: {
                        $sum:
                        {
                            $cond: [
                                {
                                    $and: [
                                        { $eq: ["$activity.activity_info.saved", true] },
                                        { $eq: ["$user_id", user_id] }]
                                }, 1, 0]
                        }
                    },
        
                    is_liked_feed: {
                        $sum:
                        {
                            $cond: [
                                {
                                    $and: [
                                        { $eq: ["$activity.activity_info.liked", true] },
                                        { $eq: ["$user_id", user_id] }]
                                }, 1, 0]
                        }
                    },
        
                    is_disliked_feed: {
                        $sum:
                        {
                            $cond: [
                                {
                                    $and: [
                                        { $eq: ["$activity.activity_info.disliked", true] },
                                        { $eq: ["$user_id", user_id] }]
                                }, 1, 0]
                        }
                    },
        
                    num_feed_visited: { $sum: { $cond: [{ $eq: ["$activity.activity_info.visit", true] }, 1, 0] } },
        
                    num_feed_liked: { $sum: { $cond: [{ $eq: ["$activity.activity_info.liked", true] }, 1, 0] } },
        
                    num_feed_disliked: { $sum: { $cond: [{ $eq: ["$activity.activity_info.disliked", true] }, 1, 0] } },
        
                    num_feed_shared: { $sum: { $cond: [{ $eq: ["$activity.activity_info.shared", true] }, 1, 0] } },
                    commentCount: { $first: "$comment.commentCount" },
                }
            }, {
                $project: {
                    user_id: "$user_id",
                    is_saved_feed: "$is_saved_feed",
                    num_feed_visited: "$num_feed_visited",
                    upvotecount: "$num_feed_liked",
                    downvotecount: "$num_feed_disliked",
                    sharecount: "$num_feed_shared",
                    is_liked: "$is_liked_feed",
                    is_disliked: "$is_disliked_feed",
                    feedComments: "$commentCount",
        
                }
            }
        
        ]).exec(function (err, userList) {
            if (err) {
                reject(err);
            } else {
                resolve(userList);
            }
        })
    })
}


const getItemInfos = (itemIds, itemData, res, next) => {
    let tasks = [];
    itemIds.forEach((item) => {
        tasks.push(
            function (pcallback) {
                let url = FeedServer.feed_details_by_id + `%7B"item_id_list":[%7B"item_id":${item}%7D]%7D`;
                Logger.logInfo(url,{});
                axios.get(url)
                    .then((response) => {
                        let itemAnalytics = itemData.find(i => i._id == item);
                        console.log("item analytics->>", itemAnalytics)
                        const {data} = response;
                        let itemInfo = {...data.item_id_info, ...itemAnalytics, _id : item};
                        pcallback(null, {...data, item_id_info: itemInfo});
                    }).catch((err) => {
                    console.log("err in itemifo-->>", err)
                    pcallback(err);
                });
            }
        )
    });
    async.parallel(tasks, function (err, results) {
        if (err) {
            return next(setError(MSG.INTERNAL_ERROR, 500));
        }
        return res.send({data: results, message: MSG.DATA_FOUND});
    })
}
const getAcivityByUserNItem = (user_id, itemId) => {
    return new Promise((resolve, reject) => {
        Models.UserActivity.aggregate([
            {$match: {'user_id': user_id}},
            {$unwind: '$activity'},
            {$match: {'activity.item_id': Number(itemId)}},
        ]).then(data => {
            if (data && data.length > 0) {
                resolve(data[0]);
            } else {
                resolve();
            }
        }).catch((err) => {
            reject(err);
        })
    })
}

const getAcivityByUser = (user_id) => {
    return new Promise((resolve, reject) => {
        Models.UserActivity.aggregate([
            {$match: {'user_id': user_id}},
        ]).then(data => {
            if (data && data.length > 0) {
                resolve(data[0]);
            } else {
                resolve();
            }
        }).catch((err) => {
            reject(err);
        })
    })
}
const getActivityInfo = (info) => {
    return {
        shared: false,
        liked: false,
        disliked: false,
        saved: false,
        rating: 0,
        tot_dur: 0,
        visit: false,
        ...info
    }
}
const getActivityObj = (user_id, itemId, info) => {
    return new Models.UserActivity({
        user_id: user_id,
        activity: [{
            item_id: itemId,
            activity_info: getActivityInfo(info),
        },],
    });
}
const updateActivity = (activity_id, updateInfo) => {
    return new Promise((resolve, reject) => {
        Models.UserActivity.updateOne({
                "activity._id": ObjectId(activity_id)
            }, {
                $set: updateInfo,
            },
            (err, update) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(update);
                }
            })
    })
}

const pushActivity = (_id, activity_info, item_id) => {
    console.log("activity_info.toObject()", activity_info);
    return new Promise((resolve, reject) => {
        Models.UserActivity.updateOne({
                "_id": ObjectId(_id)
            },
            {
                $addToSet: {activity: {activity_info: activity_info, item_id: item_id}},
            },
            (err, update) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(update);
                }
            })
    })
}
const UpdateLikeInformation = (req, res, next) => {
    const {
        id
    } = req.params;
    const {  liked= true } = req.body;
    const {user} = req;
    const userId = user.id;
    const activity = getActivityObj(userId, id, {liked: liked})
    getAcivityByUserNItem(userId, id).then((dbActivity) => {
        if (!dbActivity) {
            getAcivityByUser(userId).then((dbActivity1) => {
                if (!dbActivity1) {
                    activity.save((err, cb) => {
                        if (err) {
                            Logger.error(`error in updating like information for user: "${userId}"`);
                            return next(setError(err));
                        } else {
                            Models.UserActivity.pushUserActivities(userId,id);
                            Logger.logInfo(`success in updating like information for user: "${userId}"`);
                            return res.send({
                                data: cb._id,
                                message: MSG.SUCCESS
                            });
                        }
                    });
                } else {
                    pushActivity(dbActivity1._id, getActivityInfo({liked: liked}), id).then((data) => {
                        if (!data) {
                            return next(setError(MSG.DATA_NOT_FOUND));
                        } else {
                            Models.UserActivity.pushUserActivities(userId,id);
                            Logger.logInfo(`success in updating like information for user: "${userId}"`);
                            return res.send({
                                data: data,
                                message: MSG.SUCCESS,
                            });
                        }
                    }).catch((err) => {
                        Logger.error(`error in updating like information for user: "${userId}"`, err);
                        return next(setError(MSG.INTERNAL_ERROR, 500));
                    });
                }
            })
        } else {
            let activity_id = dbActivity.activity._id;
            let updateInfo = {
                "activity.$.activity_info.liked": liked,

            };
            if(liked){
                updateInfo["activity.$.activity_info.disliked"] = !liked;
            }
            updateActivity(activity_id, updateInfo).then((data) => {
                if (!data) {
                    return next(setError(MSG.DATA_NOT_FOUND));
                } else {
                    Models.UserActivity.pushUserActivities(userId,id);
                    Logger.logInfo(`success in updating like information for user: "${userId}"`);
                    return res.send({
                        data: data,
                        message: MSG.SUCCESS,
                    });
                }
            }).catch((err) => {
                Logger.error(`error in updating like information for user: "${userId}"`);
                return next(setError(MSG.INTERNAL_ERROR, 500));
            })
        }
    })
};

const UpdateDisLikeInformation = (req, res, next) => {
    const {
        id
    } = req.params;
    const {  disliked= true } = req.body;
    const {user} = req;
    const userId = user.id;
    const activity = getActivityObj(userId, id, {disliked: disliked})
    getAcivityByUserNItem(userId, id).then((dbActivity) => {
        if (!dbActivity) {
            getAcivityByUser(userId).then((dbActivity1) => {
                if (!dbActivity1) {
                    activity.save((err, cb) => {
                        if (err) {
                            Logger.error(`error in updating dislike information for user: "${userId}"`);
                            return next(setError(err));
                        } else {

                            Models.UserActivity.pushUserActivities(userId,id);
                            Logger.logInfo(`success in updating dislike information for user: "${userId}"`);
                            return res.send({
                                data: cb._id,
                                message: MSG.SUCCESS
                            });
                        }
                    });
                } else {
                    pushActivity(dbActivity1._id, getActivityInfo({disliked: disliked}), id).then((data) => {
                        if (!data) {
                            return next(setError(MSG.DATA_NOT_FOUND));
                        } else {
                            Models.UserActivity.pushUserActivities(userId,id);
                            Logger.logInfo(`success in updating dislike information for user: "${userId}"`);
                            return res.send({
                                data: data,
                                message: MSG.SUCCESS,
                            });
                        }
                    }).catch((err) => {
                        Logger.error(`error in updating dislike information for user: "${userId}"`);
                        return next(setError(MSG.INTERNAL_ERROR, 500));
                    });
                }
            })
        } else {
            let activity_id = dbActivity.activity._id;
            let updateInfo = {
                "activity.$.activity_info.disliked": disliked,

            };
            if(disliked){
                updateInfo["activity.$.activity_info.liked"] = !disliked;
            }
            updateActivity(activity_id, updateInfo).then((data) => {
                if (!data) {
                    return next(setError(MSG.DATA_NOT_FOUND));
                } else {
                    Models.UserActivity.pushUserActivities(userId,id);
                    Logger.logInfo(`success in updating dislike information for user: "${userId}"`);
                    return res.send({
                        data: data,
                        message: MSG.SUCCESS,
                    });
                }
            }).catch((err) => {
                Logger.error(`error in updating dislike information for user: "${userId}"`);
                return next(setError(MSG.INTERNAL_ERROR, 500));
            })
        }
    })
}
const UpdateSaveInformation = (req, res, next) => {
    const {
        id
    } = req.params;
    const {user} = req;
    const userId = user.id;
    const updateInfo = req.body;
    const saved = updateInfo.save_info[0].isSaved;
    const isSaved = (saved == "1" ? true : false)
    const activity = getActivityObj(userId, id, {saved: isSaved})
    getAcivityByUserNItem(userId, id).then((dbActivity) => {
        if (!dbActivity) {
            getAcivityByUser(userId).then((dbActivity1) => {
                if (!dbActivity1) {
                    activity.save((err, cb) => {
                        if (err) {
                            Logger.error(`error in updating save information for user: "${userId}"`);
                            return next(setError(err));
                        } else {
                            Models.UserActivity.pushProfileActivities(userId);
                            Models.UserActivity.pushUserActivities(userId,id);
                            Logger.logInfo(`success in updating save information for user: "${userId}"`);
                            return res.send({
                                data: cb._id,
                                message: MSG.SUCCESS
                            });
                        }
                    });
                } else {
                    pushActivity(dbActivity1._id, getActivityInfo({saved: isSaved}), id).then((data) => {
                        if (!data) {
                            return next(setError(MSG.DATA_NOT_FOUND));
                        } else {
                            Models.UserActivity.pushProfileActivities(userId);
                            Models.UserActivity.pushUserActivities(userId,id);

                            Logger.logInfo(`success in updating save information for user: "${userId}"`);
                            return res.send({
                                data: data,
                                message: MSG.SUCCESS,
                            });
                        }
                    }).catch((err) => {
                        Logger.error(`error in updating save information for user: "${userId}"`);
                        return next(setError(MSG.INTERNAL_ERROR, 500));
                    });
                }
            })
        } else {
            let activity_id = dbActivity.activity._id;
            updateActivity(activity_id, {
                "activity.$.activity_info.saved": isSaved
            }).then((data) => {
                if (!data) {
                    return next(setError(MSG.DATA_NOT_FOUND));
                } else {
                    Models.UserActivity.pushProfileActivities(userId);
                    Models.UserActivity.pushUserActivities(userId,id);
                    Logger.logInfo(`success in updating save information for user: "${userId}"`);
                    return res.send({
                        data: data,
                        message: MSG.SUCCESS,
                    });
                }
            }).catch((err) => {
                Logger.error(`error in updating save information for user: "${userId}"`);
                return next(setError(MSG.INTERNAL_ERROR, 500));
            })
        }
    })
};

const GetSavedFeeds = (req, res, next) => {
    const {user} = req;
    var user_id = user.id;
    console.log("userid--->>", user_id);

    Models.UserActivity.aggregate([
        {$match: {'user_id': user_id}},
        {$unwind: '$activity'},
        {$match: {'activity.activity_info.saved': true}},
        {$group: {_id: "$user_id", itemIds: {$addToSet: "$activity.item_id"}}}
    ]).then(data => {
        if (data && data.length > 0) {
            let savedFeed = data[0];
            // this.getFeedAnalytics(savedFeed.itemIds);
            getFeedMetaData(user_id).then(itemData => {
                getItemInfos(savedFeed.itemIds, itemData, res, next);
            }).catch(err => {
                console.log("error--->>", err);
            })
        } else {
            Logger.logInfo(`success in getting saved feed information for user: "${user_id}"`);
            return res.send({data: data, message: MSG.DATA_FOUND});
        }
    }).catch((err) => {
        Logger.error(`error in getting saved feed information for user: "${user_id}"`);
        console.log("error1--->>", err);
        return next(setError(err, 500));
    })
};

const visitFeed = (req, res, next) => {
    const {
        id
    } = req.params;
    const {user} = req;
    const userId = user.id;
    const activity = getActivityObj(userId, id, {visit: true})
    getAcivityByUserNItem(userId, id).then((dbActivity) => {
        if (!dbActivity) {
            getAcivityByUser(userId).then((dbActivity1) => {
                if (!dbActivity1) {
                    activity.save((err, cb) => {
                        Models.UserActivity.pushProfileActivities(userId);
                        Models.UserActivity.pushUserActivities(userId,id);
                        if (err) {
                            Logger.error(`error in updating visit feed information for user: "${userId}"`);
                            return next(setError(err));
                        } else {
                            Logger.logInfo(`success in updating visit feed information for user: "${userId}"`);
                            return res.send({
                                data: cb._id,
                                message: MSG.SUCCESS
                            });
                        }
                    });
                } else {
                    pushActivity(dbActivity1._id, getActivityInfo({visit: true}), id).then((data) => {
                        if (!data) {
                            return next(setError(MSG.DATA_NOT_FOUND));
                        } else {
                            Models.UserActivity.pushProfileActivities(userId);
                            Models.UserActivity.pushUserActivities(userId,id);
                            Logger.logInfo(`success in updating visit feed information for user: "${userId}"`);
                            return res.send({
                                data: data,
                                message: MSG.SUCCESS,
                            });
                        }
                    }).catch((err) => {
                        Logger.error(`error in updating visit feed information for user: "${userId}"`);
                        return next(setError(MSG.INTERNAL_ERROR, 500));
                    });
                }


            })
        } else {
            let activity_id = dbActivity.activity._id;
            updateActivity(activity_id, {
                "activity.$.activity_info.visit": true
            }).then((data) => {
                if (!data) {
                    return next(setError(MSG.DATA_NOT_FOUND));
                } else {
                    Models.UserActivity.pushProfileActivities(userId);
                    Models.UserActivity.pushUserActivities(userId,id);

                    Logger.logInfo(`success in updating visit feed information for user: "${userId}"`);
                    return res.send({
                        data: data,
                        message: MSG.SUCCESS,
                    });
                }
            }).catch((err) => {
                Logger.error(`error in updating visit feed information for user: "${userId}"`);
                return next(setError(MSG.INTERNAL_ERROR, 500));
            })
        }
    })
};

const GetALLUserActivities = (req, res, next) => {
    let page = req.body.pageNo;
    let pageNo = parseInt(page);
    let record = req.body.recordsPerPage
    let recordsNo = parseInt(record);
    Models.UserActivity.find().skip(recordsNo * (pageNo - 1)).limit(recordsNo).then((userList) => {
        if (!userList) {
            return next(setError(MSG.DATA_NOT_FOUND));
        } else {
            return res.send({
                data: userList,
                count: recordsNo,
                message: MSG.DATA_FOUND
            });
        }
    }).catch((err) => {
        console.log("User list err: ", err);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    });
}

const userProfileAnalytics = (req, res, next) => {
    const userId = req.body.user_id
    console.log("add data-->>>", req.body);
    Models.UserProfileAnalytics.updateProfileActivities(userId,req.body).then((cb)=>{
        return res.send({
            data: cb,
            message: MSG.SUCCESS
        });
    }).catch((err)=>{
        Logger.error(`error in updating user profile analytics information`);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    })
};

const GetUserProfileAnalytics = (req, res, next) => {
    let recordsNo = parseInt(req.body.pageSize);
    let pageNo = parseInt(req.body.pageNo);
    let start = recordsNo * (pageNo - 1);
    let limit = recordsNo;
    Models.UserActivity.aggregate([
        {
            $lookup: {
                from: "users",
                localField: "user_id",
                foreignField: "id",
                as: "usersInformation"
            }
        },
        {$unwind: {path: "$usersInformation", preserveNullAndEmptyArrays: true}},
        {$unwind: {path: "$activity", preserveNullAndEmptyArrays: true}},
        {
            $group: {
                _id: "$user_id",

                num_saved_feed: {$sum: {$cond: [{$eq: ["$activity.activity_info.saved", true]}, 1, 0]}},

                num_feed_visited: {$sum: {$cond: [{$eq: ["$activity.activity_info.visit", true]}, 1, 0]}},

                last_login_time: {$first: "$usersInformation.last_login_time"}

            }
        },

        {$skip: start},
        {$limit: limit},
        {
            $project: {

                _id: 0,
                "user_id": "$_id",
                // _id:0,
                profile_info: {
                    num_saved_feed: "$num_saved_feed",
                    last_login_time: {$cond: {if: "$last_login_time", then: "$last_login_time", else: ""}},
                    num_feed_visited: "$num_feed_visited",
                    total_time_spent: "$total_time_spent",
                    search_keywords: [],
                    app_version: ""
                },


            }
        }

    ]).exec(async function (err, data) {
        if (err) {
            console.log(err);
        } else if (!data) {
            return next(setError(MSG.DATA_NOT_FOUND));
        } else if (err) {
            Logger.error(`error in getting user profile analytics information`);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        } else if (data) {
            Logger.logInfo(`succcess in getting user profile analytics information`);
            return res.send({data: data, count: recordsNo, message: MSG.DATA_FOUND});
        }
    });

};

const getAllFeeds = (req, res, next) => {

    Models.Feed.find({})
        .then((results) => {
            if (!results) {
                return next(setError(MSG.DATA_NOT_FOUND));
            } else {
                return res.send({data: results, message: MSG.DATA_FOUND});
            }
        })
        .catch((err) => {
            console.log("User list err: ", err);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        });
};

const addUserActivities = (req, res, next) => {
    const activity = new Models.UserActivity({
        user_id: 696,
        activity: [{
            activity_info: {
                shared: false,
                liked: true,
                disliked: false,
                saved: false,
                rating: 0,
                tot_dur: "",
                visit: true
            },
            item_id: 2302095560822,
            flag: "false"
        }]
    })
    activity.save((err, cb) => {
        if (err) {

            return next(setError(err));
        } else {

            return res.send({
                data: cb._id,
                message: MSG.SUCCESS
            });
        }
    });
}

module.exports = {
    GetFeeds,
    UpdateLikeInformation,
    UpdateDisLikeInformation,
    UpdateSaveInformation,
    GetSavedFeeds,
    visitFeed,
    GetALLUserActivities,
    userProfileAnalytics,
    GetUserProfileAnalytics,
    getAllFeeds,
    addUserActivities,
    GetFeedIds,
    GetFeedData
};
