const Schema = Mongoose.Schema;
const CommentActivitySchema = Mongoose.Schema({
  comment: { type: Schema.Types.ObjectId, ref: "comment" },
  user: { type: Schema.Types.ObjectId, ref: "user" },
  like: { type: Boolean, default: false },
  dislike: { type: Boolean, default: false },
  updated_at: { type: Date, default: Date.now },
  view: { type: Boolean, default: false },
});

module.exports = Mongoose.model("CommentActivity", CommentActivitySchema);
