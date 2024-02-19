let Config = require('config'); 
if(process.env.DATABASE_URL){
    Config.Database.URL = process.env.DATABASE_URL;
}
if(process.env.DATABASE_DEBUG){
    Config.Database.Debug = process.env.DATABASE_DEBUG;
}
if(process.env.DATABASE_DBNAME){
    Config.Database.dbName= process.env.DATABASE_DBNAME;
}

if(process.env.WHITELISTDOMAINS){
    Config.SecureAccess.whitelistDomains = process.env.WHITELISTDOMAINS.split(",");
}
if(process.env.SECUREACCESS_ENABLE){
    Config.SecureAccess.enable = process.env.SECUREACCESS_ENABLE;
}
if(process.env.APPPORT){
    Config.App.PORT = process.env.APPPORT;
}
if(process.env.ADMIN_PORT){
    Config.App.ADMIN_PORT = process.env.ADMINPORT;
}
if(process.env.SITE_NAME){
    Config.App.SiteName = process.env.SITE_NAME;
}
if(process.env.SITE_SORT_NAME){
    Config.App.SiteSortName = process.env.SITE_SORT_NAME;
}
if(process.env.SECRET){
    Config.App.secret = process.env.SECRET;
}
if(process.env.KEY){
    Config.App.key = process.env.KEY;
}
if(process.env.IV){
    Config.App.iv = process.env.IV;
}
if(process.env.TOKEN_EXPIRES_TIME){
    Config.App.tokenExpiresTime = process.env.TOKEN_EXPIRES_TIME;
}
if(process.env.SEND_GRID_API_KEY){
    Config.SendGrid.SendgridAPIKey = process.env.SEND_GRID_API_KEY;
}
if(process.env.FEED_BY_USER_URL){
    Config.FeedServer.feed_by_user = process.env.FEED_BY_USER_URL;
}
if(process.env.FEED_DETAILS_BY_ID_URL){
    Config.FeedServer.feed_details_by_id = process.env.FEED_DETAILS_BY_ID_URL;
}
if(process.env.GOOGLE_ANALYTICS_KEY){
    Config.GoogleAnalytics.tid = process.env.GOOGLE_ANALYTICS_KEY;
}

if(process.env.TWILIO_ACCOUNTSID){
    Config.Twilio.AccountSID = process.env.TWILIO_ACCOUNTSID;
}
if(process.env.TWILIO_AUTHTOKEN){
    Config.Twilio.AuthToken = process.env.TWILIO_AUTHTOKEN;
}
if(process.env.TWILIO_FROM){
    Config.Twilio.From = process.env.TWILIO_FROM;
}
if(process.env.TWILIO_SERVICEID){
    Config.Twilio.ServiceID = process.env.TWILIO_SERVICEID;
}
if(process.env.TWILIO_TEMPLATEID){
    Config.Twilio.TemplateID = process.env.TWILIO_TEMPLATEID;
}
if(process.env.TWILIO_EMAILFROM){
    Config.Twilio.EmailFrom = process.env.TWILIO_EMAILFROM;
}
if(process.env.TWILIO_FROMNAME){
    Config.Twilio.FromName = process.env.TWILIO_FROMNAME;
}
if(process.env.KAFKA_SERVER_IP){
    Config.Kafka.SERVER_IP = process.env.KAFKA_SERVER_IP;
}
if(process.env.KAFKA_SERVER_PORT){
    Config.Kafka.PORT = process.env.KAFKA_SERVER_PORT;
}
if(process.env.SWAGGER_PROTOCOL){
    Config.Swagger.protocol = process.env.SWAGGER_PROTOCOL;
}
if(process.env.SWAGGER_BASE_URL){
    Config.Swagger.baseUrl = process.env.SWAGGER_BASE_URL;
}
if(process.env.SWAGGER_USER_PORT){
    Config.Swagger.userPort = process.env.SWAGGER_USER_PORT;
}
if(process.env.SWAGGER_FEED_PORT){
    Config.Swagger.feedPort = process.env.SWAGGER_FEED_PORT;
}
if(process.env.SWAGGER_CHAT_PORT){
    Config.Swagger.chatPort = process.env.SWAGGER_CHAT_PORT;
}
console.log("Config",Config)
global.Config = Config;