const Schema = Mongoose.Schema;
const { USER_ACTIVITY_TOPIC,USER_PROFILE_ANALYTICS_TOPIC } = Config.get('Kafka');
const UserActivitySchema = Schema({
        user_id: {type: Number},
        activity: [
            {
                item_id: {type: Number},
                activity_info: {
                    shared: {type: Boolean, default: false},
                    liked: {type: Boolean, default: false},
                    disliked: {type: Boolean, default: false},
                    saved: {type: Boolean, default: false},
                    rating: {type: Number, default: 0},
                    tot_dur: {type: Number, default: 0},
                    visit: {type: Boolean, default: false}
                }
            }
        ],


    },
    {
        timestamps: true,
        id: false,
        toObject: {
            virtuals: true,
            getters: true
        },
        toJSON: {
            virtuals: true,
            getters: true
        }
    }
)
UserActivitySchema.statics.pushProfileActivities = (userId) => {
    Models.UserActivity.aggregate([
        {$match: {user_id: userId}},
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
        {
            $project: {
                _id: 0,
                "user_id": "$_id",
                profile_info: {
                    num_saved_feed: "$num_saved_feed",
                    last_login_time: {$cond: {if: "$last_login", then: "$last_login", else: ""}},
                    num_feed_visited: "$num_feed_visited",
                    total_time_spent: "$total_time_spent",
                    search_keywords: [],
                    app_version: "0.0.1"
                },
            }
        }
    ]).exec(async function (err, data) {
        if (!err && data.length > 0) {
            Kafka.send(USER_PROFILE_ANALYTICS_TOPIC, data[0]);
        }
    })
}
UserActivitySchema.statics.pushUserActivities = (userId,itemId) => {

    Models.UserActivity.aggregate([
        {$match: {'user_id': userId}},
        {$unwind: '$activity'},
        {$match: {'activity.item_id': Number(itemId)}},
    ]).then(activities => {
        if (activities && activities.length > 0) {
           Kafka.send(USER_ACTIVITY_TOPIC, activities[0]);
        }
    }).catch((err) => {
        console.log("error-->>", err);
    });
}
module.exports = Mongoose.model('UserActivity', UserActivitySchema);