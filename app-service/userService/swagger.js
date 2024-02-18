require('../config/config');
const swaggerAutogen = require('swagger-autogen')()
const { Swagger= {} } = Config;
const { baseUrl , userPort, protocol, userBasePath} = Swagger
const uri = baseUrl+":"+userPort;
const doc = {
    info: {
        version: "1.0.0",
        title: "User service server",
        description: "User service"
    },
    host:uri,
	basePath: userBasePath,
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

const outputFile = './userService/swagger_output.json'
                    
const endpointsFiles = [
    "./userService/src/controller/users.js",
    "./userService/src/controller/interests.js"
    
];

swaggerAutogen(outputFile, endpointsFiles, doc).then(() => {
    require('./bin/www') // Your project's root file
});
