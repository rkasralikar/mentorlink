const Schema = Mongoose.Schema;
const bcrypt = require('bcryptjs');
const saltRounds = 10;
const { DEFAULT_USER_IMAGE, USER_STATUS }=require("../../../config/constants")
const AutoIncrement = require('mongoose-sequence')(Mongoose);
const UserSchema = Mongoose.Schema(
    {
        email: { type: String, unique: true, sparse: true},
        secondary_email: { type: String },
        password: String,
        role: String,
        userid: { type: Schema.Types.ObjectId },
        first_name: { type: String, trim: true },
        middle_name: { type: String, trim: true },
        last_name: { type: String, trim: true },
        name: String,
        image: {
            type: String,
            default: DEFAULT_USER_IMAGE
        },
        phone: {type:String,default:""},
        linkedin_profile:{type:String,default:""},
        activation_key: String,
        activation_key_expire_date: Date,
        otp: String,
        otp_expire_date: Date,
        password_reset_key: String,
        is_deleted: { type: Boolean, default: false },
        status: { type: Number, default: USER_STATUS.NEW },
        is_primary: { type: Boolean, default: false },
        is_verified: { type: Boolean, default: false },
        verified_date: { type: Date },
        term_accepted: { type: Boolean, default: false },
        last_login: { type: Date, default: null },
        created_at: { type: Date },
        updated_at:{ type: Date },
        gender:{ type: String },
        location: { type: Array },
        skills: { type: Schema.Types.Array },
        interests: { type: Schema.Types.Array },
        career_summary: { type: String },
        mentor_link_account_number: { type: String },
        contacts: { type: Array },
        group_indicator: { type: Array },
        sign_in_method: { type: String },
        ssid : {type :String ,default:""},
        is_linkedin_visited : {type: Boolean, default: false},
        is_active : {type : Boolean , default : true},
        is_new : {type : Boolean},
        is_mentor: {type: Boolean ,default : false},
        is_career_summary : {type : String ,default :true},
        update24hrsTime: {type:Date,default:""},
        device_data : [{
            deviceId : {type :String ,default : ""},
            osVersion : {type :String ,default : ""},
            osType: {type :String ,default : ""},
            deviceName : {type :String ,default : ""},
            deviceToken : {type :String ,default : ""}
        }],
        last_login_time : {type:Date,default:""},
        recent_seen_time:{ type: Date  }
    },
    {
        timestamps: true,
        id: false,
        toObject: {
            virtuals: true,
            getters: true
        },
        toJSON: {
            virtuals: true,
            getters: true
        }
    }
);
UserSchema.post('init', function() {
    this._original = this.toObject();
});
UserSchema.pre('save', function(next) {
    this.wasNew = this.isNew;
    if (!empty(this.first_name) && !empty(this.last_name) && !empty(this.middle_name)) {
        this.name =
            this.first_name.trim() + ' ' + this.middle_name.trim() + ' ' + this.last_name.trim();
    } else if (!empty(this.first_name) && !empty(this.last_name)) {
        this.name = this.first_name.trim() + ' ' + this.last_name.trim();
    }
    if ((!empty(this.password) && this.isNew) || this.isModified('password')) {
        const document = this;
        bcrypt.hash(this.password, saltRounds, function(err, hashedPassword) {
            if (err) {
                next(err);
            } else {
                document.password = hashedPassword;
                next();
            }
        });
    } else {
        next();
    }
});
UserSchema.post('save', function() {
    if (this.wasNew) {
        let CounterUser = Mongoose.model('Counter_user_count');
        CounterUser.findOneAndUpdate(
            {id: 'user_count', reference_value: null},
            {$inc: {seq: 1}},
            {
                upsert: true,
                new: true
            },
            (err, counter) => {
                Models.User.updateOne(
                    {_id: this._id},
                    {$set: {id: counter.seq}},
                    (err, result) => {
                    }
                );
            }
        );
    }

});
UserSchema.statics.updateLastLogin = function(userId) {
    Models.User.findOneAndUpdate({ _id: userId }, { $set: { last_login: new Date(),status:USER_STATUS.ACTIVE} }, function(
        err,
        res
    ) {});
};

UserSchema.statics.setActivatedBy = function (userId) {
    Models.User.findOneAndUpdate({ _id: userId }, { $set: { activated_by: 'User'} }, function(
        err,
        res
    ) {});
};
UserSchema.methods.isCorrectPassword = function(password, callback) {
    bcrypt.compare(password, this.password, function(err, same) {
        if (err) {
            callback(err);
        } else {
            callback(err, same);
        }
    });
};
UserSchema.plugin(AutoIncrement, {
    id: 'user_count',
    inc_field: 'id',
    disable_hooks: true
});
UserSchema.index({status:1});
UserSchema.index({name:'text',status:1,role:1},{name:'user_text_search'});
UserSchema.index({name:1});
module.exports = Mongoose.model('User', UserSchema);
