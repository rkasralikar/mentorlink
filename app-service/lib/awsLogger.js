const winston = require('winston');
const logger = new winston.createLogger({
    format: winston.format.json(),
    transports: [
        new (winston.transports.Console)({
            timestamp: true,
            colorize: true,
        })
    ]
});

logger.insert = (type, req, err = {}) => {
    if (Config.get('AWS.CloudWatchLog')) {
        const {loggerId = ''} = req;
        const {password = '', ...bodyInfo} = req.body;
        if (password) {
            bodyInfo.password = '******';
        }
        if (type === 'error') {
            logger.log('error', `${loggerId} Origin ${req.origin} Requesting ${req.method} ${req.originalUrl}`, {
                tags: 'https',
                additionalInfo: {body: bodyInfo, headers: req.headers, stack: err.stack}
            });
        } else if (type === 'info') {
            logger.log('info', `${loggerId} Origin ${req.origin} Requesting ${req.method} ${req.originalUrl}`, {
                tags: 'https',
                additionalInfo: {body: bodyInfo, headers: req.headers}
            });
        }
    } else {
        console.log(err);

    }
};
logger.log1 = (type, message, err = {}) => {
    if (Config.get('AWS.CloudWatchLog')) {
        if (type === 'error') {
            logger.log('error', `${message}`, {
                tags: 'https',
                additionalInfo: {body: message}
            });
        } else if (type === 'info') {
            logger.log('info', `${message}`, {tags: 'https'});
        }
    } else {
        console.log(type, err);

    }
};

logger.logInfo = (message, err = {}) => {
    if (Config.get('AWS.CloudWatchLog')) {
        logger.log('info', `${message}`, );
    } else {
        console.log(err);

    }
};

module.exports = logger;
