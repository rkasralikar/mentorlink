const DEFAULT_USER_IMAGE = "user.png";

const USER_STATUS = {
    IN_ACTIVE: 0,
    ACTIVE: 1,
    NEW: 3,
    INVITED: 4,
    ON_HOLD: 6,
    DNC:9
};

const GOOGLE_ANALYTICS = {
    PAGE_VIEW: "pageview",
    EVENT: "event",
    SCREEN_VIEW: "screenview"
};

module.exports = {
    DEFAULT_USER_IMAGE,
    USER_STATUS,
    GOOGLE_ANALYTICS
};
