global.Mongoose = require('mongoose');
global.ObjectId = Mongoose.Types.ObjectId;
const  dbConfig = Config.get('Database');
const options = {
    useCreateIndex: true,
    useNewUrlParser: true,
    dbName: dbConfig.dbName,
    poolSize: 25,
    reconnectTries: 60,
    reconnectInterval: 1000,
    bufferMaxEntries: 0,
    useUnifiedTopology: true,
    useFindAndModify: false,
};
Mongoose.connect(dbConfig.URL, options);
const mongodb = Mongoose.connection;
mongodb.on('error', console.error.bind(console, 'connection error:'));
mongodb.once('open', function() {
    console.log('db connection developed.');
});
const ChatMessage = require("./chatMessage");
const ChatRoom = require("./chatRoom");


console.log("her in the chat indexx.js")
Mongoose.set('debug', dbConfig.Debug);
let database = {ChatRoom:ChatRoom,ChatMessage:ChatMessage};
Mongoose.set('useFindAndModify', false);
database.mongoose = Mongoose;
module.exports = database;
