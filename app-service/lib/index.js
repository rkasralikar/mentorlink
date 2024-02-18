let setError = (msg, code) => {
    if (msg && msg.code === 11000) {
        let keyValue = msg.keyValue;
        let field ='';
        for(key in keyValue){
            console.log(key);
            let label =MSG[key];
            field =label+" as "+keyValue[key];
        }
        msg= "Please use unique value for  " + field + " is already exists."
    }
    if (_.isUndefined(code)) {
        code = 400;
    }
    let err = new Error(msg);
    err.status = code;
    return err;
};

let empty = value => {
    if (!_.isUndefined(value)) {
        if ((typeof value == 'array' || typeof value == 'object') && _.isEmpty(value)) {
            return true;
        } else if (value == '') {
            return true;
        } else {
            return false;
        }
    }
    return true;
};
let isset = value => {
    if (!_.isUndefined(value)) {
        return true;
    }
    return false;
};
let ObjectIds = ids => {
    return _.map(ids, function(id) {
        return ObjectId(id);
    });
};

let isBetween = function(start, end, value) {
    var min = Math.min(start, end),
        max = Math.max(start, end);
    return value > min && value < max;
};
let replaceAll = function(string, search, replacement) {
    return string.split(search).join(replacement);
};
let getDomain = function(string) {
    return string.replace(/.*@/, '');
};
let isProd = function() {
    return true;//_.includes(['default', 'nd'], process.env.NODE_APP_INSTANCE);
};
let dateToString = function(object) {
    var flatten = require('flat');
    return flatten.unflatten(
        _.transform(flatten(object), function(result, value, key) {
            result[key] = _.isDate(value) ? value.toISOString() : value;
        })
    );
};

let getRole = selected => {
    return _.filter(ROLES, key => selected.includes(key))[0];
};
let getAction = method => {
    return method == 'POST' || method == 'PUT' ? 'write' : method == 'DELETE' ? 'delete' : 'read';
};
let replaceMulti = function(string, replacement) {
    _.each(replacement, (replace, search) => {
        string = string.split(search).join(replace);
    });
    return string;
};
let getFutureDay = day => {
    const dayNumber = Moment().day(day).isoWeekday();
    const today = Moment().isoWeekday();
    if (today < dayNumber) {
        return Moment().isoWeekday(dayNumber);
    } else {
        return Moment().add(1, 'weeks').isoWeekday(dayNumber);
    }
};
let dateToISO = (addSubtractDays = 0, format = 'YYYY-MM-DD', tz = DEFAUTL_TIMEZONE) => {
    return new Date(Moment().tz(tz).add(addSubtractDays, 'days').format(format));
};
let weeekStartEnd = (addSubtractWeek = 0, format = 'YYYY-MM-DD', tz = DEFAUTL_TIMEZONE) => {
    const start = new Date(Moment().tz(tz).add(addSubtractWeek, 'weeks').startOf('isoWeek').startOf('day').format(format));
    const end = new Date(Moment().tz(tz).add(addSubtractWeek, 'weeks').endOf('isoWeek').endOf('day').format(format));
    return { start, end };
};
let isoWeekEndDate = (addSubtractWeek = 0, format = 'YYYY-MM-DD', tz = DEFAUTL_TIMEZONE) => {
    return new Date(Moment().tz(tz).add(addSubtractWeek, 'isoWeek').endOf('isoWeek').format(format));
};
let isoWeekStartDate = (addSubtractWeek = 0, format = 'YYYY-MM-DD', tz = DEFAUTL_TIMEZONE) => {
    return new Date(Moment().tz(tz).add(addSubtractWeek, 'isoWeek').startOf('isoWeek').format(format));
};
let toISO = (date, format = 'YYYY-MM-DD') => {
    return new Date(Moment(date).format(format));
};
module.exports = {
    setError,
    empty,
    isset,
    isBetween,
    ObjectIds,
    replaceAll,
    getDomain,
    isProd,
    dateToString,
    getRole,
    getAction,
    replaceMulti,
    getFutureDay,
    dateToISO,
    weeekStartEnd,
    isoWeekEndDate,
    isoWeekStartDate,
    toISO
};
