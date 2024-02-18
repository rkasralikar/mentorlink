require('../config/config');
const swaggerAutogen = require('swagger-autogen')()
const { Swagger= {} } = Config;
const { baseUrl , feedPort, protocol, feedBasePath} = Swagger
const uri = baseUrl;
const doc = {
    info: {
        version: "1.0.0",
        title: "Feed service server",
        description: "Feed service"
    },
    host:uri,
	basePath: feedBasePath,
    schemes: [ protocol ],
    consumes: ['application/json'],
    produces: ['application/json'],
    tags: [],
    securityDefinitions: {
        api_key: {
            type: "token",
            name: "x-access-token",
            in: "header"
        }
    },
    definitions: {}
};

const outputFile = './feedService/swagger_output.json'
                    
const endpointsFiles = [
    "./feedService/src/controller/feed.js",
    "./feedService/src/controller/comment.js",
     
];

swaggerAutogen(outputFile, endpointsFiles, doc).then(() => {
    require('./bin/www') // Your project's root file
});
