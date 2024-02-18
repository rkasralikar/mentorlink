const createError = require('http-errors');
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const swaggerUi = require('swagger-ui-express');
let swaggerFile = require('./swagger_output.json');
require('../config/config');
const {setError,empty,getRole} = require("../lib");
global.MSG = require("../local/en/message");
global.Models = require('./src/models');
//global.Model = require('../userService/src/models/user')
global._ = require('lodash');
global.Func = require('../lib/Functions');
global.Logger = require('../lib/awsLogger');
global.setError=setError;
global.getRole = getRole;
global.empty = empty;
//global.Rules = require('./validation/rules');
global.Validator = require('validatorjs');

global.Analytics = require('../middleware/analytics');
global.auth = require('../middleware/auth');

const admin = require("firebase-admin");
const serviceAccount = require("./mentorlink-2d1c1-firebase-adminsdk-b3ldj-0bb554bb5e.json");

global.admin = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
const indexRouter = require('./src/controller/index');
const chatRouter = require('./src/controller/chatController');
const app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
//Whenever someone connects this gets executed
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(function(req, res, next) {
  req.loggerId = Math.floor(10000 + Math.random() * 10000);
  res.header('Access-Control-Allow-Origin', '*');
  Logger.insert('info',req,{});
  next();
})
app.use('/', indexRouter);
app.use('/chats', chatRouter);

app.use('/chat-api-docs', (req, res, next)=>{
  const fullUrl = req.protocol + '://' + req.get('host')
  swaggerFile.host=fullUrl;
   console.log("swaggerFile", swaggerFile.host);
  next();
},swaggerUi.serve, swaggerUi.setup(swaggerFile));

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  Logger.insert('error',req,err);
  res.status(err.status || 500);
  res.send({message:err.message});
});

// Capture 404 erors
app.use((req,res,next) => {
  res.status(404).send("PAGE NOT FOUND");
  Logger.insertInfo('error',`400 || ${res.statusMessage} - ${req.originalUrl} - ${req.method} - ${req.ip}`);
})
module.exports = app;
