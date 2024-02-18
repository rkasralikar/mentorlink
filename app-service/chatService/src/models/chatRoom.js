const Schema = Mongoose.Schema;
const mongoose = require("mongoose");
const AutoIncrement = require("mongoose-sequence")(Mongoose);

const { v4 } = require("uuid");
const uuidv4 = v4;

const chatRoomSchema = Mongoose.Schema(
  {
    userIds: [{ type: Schema.Types.ObjectId }],
    type: { type: String },
    lastMessage: { type: String, default: "" },
    messageType: { type: String, default: "" },
    id: [{ type: Number }],
    groupNumber: { type: Number, default: 0 },
    chat_initiator: { type: Number, default: 1 },
  },
  {
    timestamps: true,
    collection: "chatrooms",
  }
);

chatRoomSchema.plugin(AutoIncrement, {
  id: "group_seq",
  inc_field: "groupNumber",
});

chatRoomSchema.index({userIds:1});
chatRoomSchema.index({id:1});
module.exports = Mongoose.model("ChatRoom", chatRoomSchema);
