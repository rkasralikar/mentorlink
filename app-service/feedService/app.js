const createError = require('http-errors');
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const swaggerUi = require('swagger-ui-express');
let swaggerFile = require('../feedService/swagger_output.json');
const {setError,empty,getRole} = require("../lib");
require('../config/config');
global.MSG = require("../local/en/message");
global.Models = require('./src/models');

global.empty = empty;
global._ = require('lodash');
global.Func = require('../lib/Functions');
global.Logger = require('../lib/awsLogger');
global.Kafka = require("./src/service/kafkaService")

//global.Rules = require('./validation/rules');
global.Validator = require('validatorjs');
global.setError=setError;
global.getRole = getRole;
global.Analytics = require('../middleware/analytics');
global.JSONSchema = require('../middleware/schema');
global.validator = require('../middleware/validator');
global.auth = require('../middleware/auth');
global.STATUS_CODE = require("../config/responseCode");



const indexRouter = require('./src/controller/index');
const feedRouter = require('./src/controller/feed');
const commentRouter = require('./src/controller/comment');


const app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.use(logger('dev'));

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/', indexRouter)
app.use('/feeds', feedRouter);
app.use('/feeds/comments', commentRouter);



app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'x-access-token,x-timezone,Content-Type, x-portal');
  res.header('Access-Control-Max-Age', 1728000);
  req.body;
  next();
});
app.use('/feed-api-docs', (req, res, next)=>{
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
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.send({ message: err.message });
});



module.exports = app;
