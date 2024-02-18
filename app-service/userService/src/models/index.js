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
const User = require("./user");
const Interest = require('./interests');
const SystemAlert = require('./systemAlert');

Mongoose.set('debug', dbConfig.Debug);
let database = {User: User,Interest:Interest, SystemAlert:SystemAlert};
Mongoose.set('useFindAndModify', false);
database.mongoose = Mongoose;
module.exports = database;
