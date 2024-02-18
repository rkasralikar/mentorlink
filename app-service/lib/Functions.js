const randomize = require("randomatic");
const bcrypt = require('bcryptjs');

module.exports = {
    validate: function (rules) {
        return function (req, res, next) {
            var validation = new Validator(req.body, rules);
            if (validation.fails()) {
                if (!_.isUndefined(req.files) && !_.isEmpty(req.files)) {
                    _.each(req.files, function (file) {
                        Func.deleteFile(file.path);
                    });
                }
                var error = validation.errors.all();
                return next(setError(error[Object.keys(error)[0]][0]));
            } else {
                return next();
            }
        };
    },
    uploadOnS3: function(params) {
        let { fileKey, body, url, type = 'url', is_public = true } = params;
        return new Promise(function(fulfill, reject) {
            var AWS = require('aws-sdk');
            const s3Options = {
                accessKeyId: Config.AWS.AccessKey,
                secretAccessKey: Config.AWS.SecretKey
            };
            const s3 = new AWS.S3(s3Options);
            if (type == 'url') {
                body = Fs.readFileSync(url);
            }
            let params = {
                Bucket: Config.AWS.Bucket,
                Key: fileKey,
                Body: body
            };
            if (is_public) {
                params.ACL = 'public-read';
            }
            s3.upload(params, (err, data) => {
                if (err) {
                    reject(err);
                } else {
                    fulfill(Func.CFNPath(data.Location));
                }
            });
        });
    },
    CFNPath: (s3url) => {
        const url = new URL(s3url);
        const S3Url = new URL(Config.AWS.S3Path);
        url.hostname = S3Url.hostname;
        return url.href || '';
    },
    getS3FileAsBase64FormatByFileURL: function(fileUrl) {
        return new Promise(function(fulfill, reject) {
            axios.get(fileUrl, { responseType: 'arraybuffer' }).then(response => {
                const { data = '', status = 0, statusText = '' } = response || {};
                if (status === 200) {
                    let content = Buffer.from(data, 'binary').toString('base64');
                    fulfill(content);
                } else {
                    reject(statusText);
                }
            }).catch(error => {
                reject(error);
            });
        });
    },
    getS3FileKeyByFileURL: function(fileUrl) {
        let URL = require('url').URL;
        let url = new URL(fileUrl);
        let pathname = url.pathname;
        let fileKey = pathname.substr(1);
        return fileKey;
    },
    getObjectOnS3: function(params) {
        let { source, bucket = Config.AWS.Bucket } = params;
        return new Promise(function(fulfill, reject) {
            var AWS = require('aws-sdk');
            const s3Options = {
                accessKeyId: Config.AWS.AccessKey,
                secretAccessKey: Config.AWS.SecretKey
            };
            const s3 = new AWS.S3(s3Options);
            let params = {
                Bucket: bucket,
                Key: source,
            };
            s3.getObject(params, (err, data) => {
                if(err){
                    reject(err);
                }else{
                    fulfill(data);
                }
            });
        });
    },
    getlistObjectsOnS3: function(params) {
        let { source, bucket = Config.AWS.Bucket } = params;
        return new Promise(function(fulfill, reject) {
            var AWS = require('aws-sdk');
            const s3Options = {
                accessKeyId: Config.AWS.AccessKey,
                secretAccessKey: Config.AWS.SecretKey
            };
            const s3 = new AWS.S3(s3Options);
            let params = {
                Bucket: bucket,
                Prefix: source,
                Delimiter: '/'
            };
            s3.listObjectsV2(params, (err, data) => {
                if (err) {
                    reject(MSG.INTERNAL_ERROR);
                } else {
                    fulfill(data.Contents);
                }
            });
        });
    },
    createRandomOtp: function (length = 6) {
        return randomize('0', length)
    },
    createRandomString: function(length = 6) {
        return randomize('a0', length);
    },
    otpTimeValidation: function (time, minutes=10) {
        return Moment(time).add(minutes, 'minute').isAfter(new Date());
    },
    HashPassword: function (password, callback) {
        let salt = bcrypt.genSaltSync(10);
        return bcrypt.hash(password, salt, (err, pass)=>{
            if(err){
                callback(err)
            }else {
                callback(err, pass);
            }
        });
    }
}
