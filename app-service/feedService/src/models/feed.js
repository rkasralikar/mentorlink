const Schema = Mongoose.Schema;

const FeedSchema = Mongoose.Schema(
    {
        item: {type: Object},
        name: {type: String},
        description: {type: String},
        item_id: {type: Number}
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
);

module.exports = Mongoose.model('Feed', FeedSchema);
