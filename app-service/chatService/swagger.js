require('../config/config');
const swaggerAutogen = require('swagger-autogen')()
const { Swagger= {} } = Config;
const { baseUrl , chatPort, protocol, chatBasePath} = Swagger
const uri = baseUrl+":"+chatPort;
const doc = {
    info: {
        version: "1.0.0",
        title: "Chat service server",
        description: "Chat service"
    },
    host: uri,
	basePath: chatBasePath,
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

const outputFile = './chatService/swagger_output.json'
                    
const endpointsFiles = [
    "./chatService/src/controller/chatController.js",
    
    
    
];

swaggerAutogen(outputFile, endpointsFiles, doc).then(() => {
    require('./bin/www') // Your project's root file
});
