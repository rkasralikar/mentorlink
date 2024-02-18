const Schema = Mongoose.Schema;

const InterestSchema = Mongoose.Schema(
    {
        name: { type: String },
        
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

module.exports = Mongoose.model('Interest', InterestSchema);
