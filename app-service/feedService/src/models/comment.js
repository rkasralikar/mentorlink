const Schema = Mongoose.Schema;
const CommentSchema = Mongoose.Schema({
  item_id: {type: Number},
  user: {type: Schema.Types.ObjectId, ref: "user"},
  comment:String,
  parent_id:{type: Schema.Types.ObjectId, ref: "comment"},
  posted_at: {type: Date, default: Date.now},
  updated_at: {type: Date, default: Date.now},
});

module.exports = Mongoose.model("Comment", CommentSchema);
