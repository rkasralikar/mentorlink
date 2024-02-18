
let secret = Config.get('App.secret');
let tokenExpiresTime = Config.get('App.tokenExpiresTime');
let User = Models.User;
let jwt = require('jsonwebtoken');

module.exports = {
    check: function(req, res, next) {
        console.log("bearer token - >",req.headers['x-access-token'])
        const token =
            req.body.token || req.query.token || req.headers['x-access-token'] || req.cookies.token;
         
            console.log("token--->>>",token);
        if (!token) {
            return next(setError(MSG.AUTH_TOKEN_EMPTY, 403));
        } else {
            jwt.verify(token, secret, function(err, decoded) {
              console.log("decoded---->>>",decoded);
                if (err) {
                    return next(setError(MSG.AUTH_TOKEN_FAILD, 403));
                } else {
                    req.user = decoded;
                    res.setHeader('x-access-token', token);
                    next();
                }
            });
        }
    },
    byPass: function(req, res, next) {
        const token =
            req.body.token || req.query.token || req.headers['x-access-token'] || req.cookies.token;

        if (!token) {
            next();
        } else {
            jwt.verify(token, secret, function(err, decoded) {
                if (err) {
                    return next(setError(MSG.AUTH_TOKEN_FAILD, 403));
                } else {
                    User.findById(decoded._id, { password: 0 }, function(err, user) {
                        if (user == null) {
                            return next(setError(MSG.USER_NOT_EXIST, 403));
                        } else if (user.is_deleted) {
                            return next(setError(MSG.LOGIN_DELETED, 403));
                        } else if (
                            user.status == USER_STATUS.IN_ACTIVE &&
                            user.activation_key == ''
                        ) {
                            return next(setError(MSG.LOGIN_DEACTIVE, 403));
                        } else {
                            req.user = user;
                            if (!empty(decoded.company_id)) {
                                req.user.company_id = ObjectId(decoded.company_id);
                            }
                            next();
                        }
                    });
                }
            });
        }
    },
    getToken: function(user) {
       console.log("user payload --->>>",user);
        let token = jwt.sign(user, secret, {
            expiresIn: tokenExpiresTime // expires in 24 hours
        });
        return token;
    },
};
