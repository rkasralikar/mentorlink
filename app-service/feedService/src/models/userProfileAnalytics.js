const Schema = Mongoose.Schema;

const UserProfileAnalyticsSchema = Mongoose.Schema({
        user_id: {type: Number, default: 0},
        profile_info: {
            num_saved_feed: {type: Number, default: 0},
            last_login_time: {type: String, default: ""},
            num_feed_visited: {type: Number, default: 0},
            total_time_spent: {type: Number, default: 0},
            search_keywords: {type: Array, default: []},
            app_version: {type: String, default: ""},
        },


    },
    {
        timestamps: true,
        id: "",
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
UserProfileAnalyticsSchema.statics.updateProfileActivities = (userId, analyticsBody) => {
    return new Promise((resolve, reject) => {
        Models.UserProfileAnalytics.findOne({user_id: userId}, (err, user) => {
            if (err) {
                reject(err);
                return;
            }
            if (!user) {
                const userProfile = new Models.UserProfileAnalytics({
                    user_id: userId,
                    profile_info: analyticsBody
                });
                userProfile.save((err, cb) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(cb);
                    }
                });
            } else {
                Models.UserProfileAnalytics.findOneAndUpdate({user_id: userId}, {$set: {"profile_info": analyticsBody}}, {new: true},
                    (err, updateCallback) => {
                        if (err) {
                            reject(err);
                        } else {
                            resolve(updateCallback);
                        }
                    })
            }
        });
    })
}
module.exports = Mongoose.model('UserProfileAnalytics', UserProfileAnalyticsSchema);