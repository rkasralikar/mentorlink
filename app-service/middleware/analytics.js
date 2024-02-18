let analyticsConfig = require("../config/default").GoogleAnalytics;
const axios = require('axios');
const { GOOGLE_ANALYTICS } = require('../config/constants');

let params = {
    v: analyticsConfig.v,
    tid: analyticsConfig.tid,
    cid: analyticsConfig.cid
};

module.exports = {
    event: async function (req, res, next) {
        let { category, action, label, value } = req.body;
        params.t = GOOGLE_ANALYTICS.EVENT;
        params.dp = req.method.toLowerCase() + req.baseUrl;
        params.ec = category;
        params.ea= action;
        params.el = label;
        params.ev = value;

        await axios.get('https://www.google-analytics.com/collect', {
            params: params
        }).then(function (response) {
            return next();
        }).catch(err =>{
            return next(setError(err, 500));
        });
    }
};
