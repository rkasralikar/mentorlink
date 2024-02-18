const auth = require("../../../middleware/auth");
let jwt = require('jsonwebtoken');

const registerUser = async (data,condition,res,next) =>{
    const {
        userid, name, email, ssid: ssid, sign_in_method, skills, interests, career_summary, location,
        created_at = new Date(), term_accepted, image, is_deleted, deviceId, osVersion, osType, deviceName,
        deviceToken, is_mentor
    } = data;
    const user = new Models.User({
        userid: ObjectId(userid),
        name: name,
        email: email,
        ssid: ssid,
        sign_in_method: sign_in_method,
        skills: skills,
        interests: interests,
        career_summary: career_summary,
        location: location,
        created_at: created_at,
        image: image,
        term_accepted: term_accepted,
        is_deleted: is_deleted,
        is_mentor: is_mentor,
        device_data: [
            {
                deviceId: deviceId,
                osVersion: osVersion,
                osType: osType,
                deviceName: deviceName,
                deviceToken: deviceToken,
            },
        ],
    });
    try {
        let dbUser = await  Models.User.findOne(condition);
        if(!dbUser){
            dbUser = await user.save();
        }else {
            if (dbUser.is_active === false) {
                return res.send({
                    status: 0,
                    message:
                        "Your Account have been deactivated please contact the concerned authority",
                });
            } else if (dbUser.is_active === true) {
                let userWithDevice = await Models.User.findOne({ _id: new ObjectId(dbUser._id),
                    "device_data": {$elemMatch: {deviceId: deviceId}}})
                if(userWithDevice){
                    await Models.User.findOneAndUpdate(
                        {
                            _id: new ObjectId(dbUser._id),
                        },
                        {
                            $push: {
                                device_data: {
                                    deviceId: deviceId,
                                    osVersion: osVersion,
                                    osType: osType,
                                    deviceName: deviceName,
                                    deviceToken: deviceToken,
                                },
                            },
                        }
                    );
                }else{
                    await Models.User.updateOne(
                        {
                            _id: new ObjectId(dbUser._id),
                            "device_data": {$elemMatch: {deviceId: deviceId}}
                        },
                        {
                            $set:
                                {
                                    "device_data.$.deviceToken": deviceToken

                                }
                        })
                }
            }
        }
        const newToken = auth.getToken({user: dbUser._id});
        return res.send({
            data: user,
            token: newToken,
            message: MSG.REGISTER_SUCCESS,
        });
    }catch (err) {
        console.log("User save err: ", err);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    }
}

const SocialMediaRegister = async (req, res, next) => {
    const { ssid } = req.body;
    return registerUser( req.body, {ssid: ssid}, res, next );
};

const RegisterWithPhone = (req, res,next) => {
    const { phone } = req.body;
    return registerUser( req.body, {phone: phone}, res,next );

};

const Register = (req, res, next) => {
    const { email } = req.body;
    return registerUser( req.body, {email: email}, res,next );
};

const UpdateRegisteredUser = async (req, res, next) => {
    const {user} = req;
    const userId = user.user;
    const UpdateInfo = req.body;
    UpdateInfo.updated_at = new Date();
    let minutesToAdd = 1440;
    let currentDate = new Date();
    UpdateInfo.update24hrsTime = new Date(currentDate.getTime() + minutesToAdd * 60000);
    try {
        const dbUser =  await Models.User.findOneAndUpdate({_id: ObjectId(userId)},
            { $set: UpdateInfo}, {new: true});
        if (UpdateInfo.interests && UpdateInfo.interests.length > 0) {
            await SaveInterest(UpdateInfo.interests, userId, next);
        }
        Logger.logInfo(`Successfully updated data for user  :"${userId}"`);
        return res.send({data: dbUser, message: MSG.SUCCESS});
    }catch (err) {
        console.log("Update dbUser err: ", err);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    }
};

const SaveInterest = async (interestsList, userId, next) => {
    const interestArray = interestsList;
    for (const interestArrayElement of interestArray) {
        try {
            let dbInterest = Models.Interest.findOne({"name": interestArrayElement});
            if(!dbInterest){
                const interests = new Models.Interest({ name: interestArrayElement, user_id: userId});
                await interests.save();
            }
        }catch (e) {
            return next(setError(MSG.INTERNAL_ERROR, 500));
        }
    }
};

const generateRegistrationToken = function (res) {

    const user = "mentorlinkUserPayload"
    let token = jwt.sign(user, "iloveBiCS21", {
        // expires in 24 hours
    });
    return res.json({
        token: token
    })
};


const GetUsers = async (req, res, next) => {
    const {user} = req;
    const userId = user.user;
    try {
        const dbUser = await Models.User.findOne({_id: ObjectId(userId)});
        Logger.logInfo(` getting data for user :"${userId}"`);
        return res.send({data: dbUser, message: MSG.DATA_FOUND});
    }catch (err) {
        console.log("User list err: ", err);
        return next(setError(MSG.DATA_NOT_FOUND));
    }
};

const TwoStepAuthentication = async (req, res, next) => {
    const MIN = 100000;
    const MAX = 999999;
    const otp = JSON.stringify(
        Math.floor(Math.random() * (MAX - MIN + 1)) + MIN
    );
    const { sendEmailOTP, sendSMSOTP } = SMS;
    if (req.body.email) {
        try {
            const verification_check = await sendEmailOTP(req.body);
            if (verification_check.status === "pending") {
                return res.json({data: otp, message: "OTP send successfully", status: true})
            }
        }catch (e) {
            console.log("TwoStepAuthentication Email", e);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        }
    } else if (req.body.phone) {
        try {
            const verification_check = await sendSMSOTP(req.body);
            if (verification_check.status === "pending") {
                return res.json({data: otp, message: "OTP send successfully", status: true})
            }
        }catch (e) {
            console.log("TwoStepAuthentication sms", e);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        }
    }
};


const sendOtp =  async (req, res, next) => {

    const MIN = 100000;
    const MAX = 999999;
    const otp = JSON.stringify(
        Math.floor(Math.random() * (MAX - MIN + 1)) + MIN
    );
    const { phone } = req.body;
    const dbUser = await Models.User.findOne({phone: phone});
    if(dbUser && dbUser.role == "Test"){
        return res.json({data: dbUser.otp, message: "OTP send successfully", status: true})
    }
    const { sendSMSOTP } = SMS;
    try {
        const verification_check = await sendSMSOTP(req.body);
        if (verification_check.status === "pending") {
            return res.json({data: otp, message: "OTP send successfully", status: true})
        }
    }catch (e) {
        console.log("TwoStepAuthentication sms", e);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    }

};

const verifyOtp = async (req, res, next) => {
    const { code, phone, email } = req.body;
    try {
        let conditions = {};
        if(phone){
            conditions = {phone: phone}
        }
        if(email){
            conditions = {email: email}
        }
        const dbUser = await Models.User.findOne(conditions);
        if(dbUser && dbUser.otp == code){
            return res.json({message: "OTP verified successfully", status: true})
        }
        const verificationChannel = phone ? phone : email
        const { verifyOTP } = SMS;
        const verification_check = await verifyOTP({verificationChannel, code});
        if (verification_check.status === "approved") {
            return res.json({message: "OTP verified successfully", status: true})
        } else if (verification_check.status === "pending") {
            return res.json({message: "Please Enter Valid OTP", status: false})
        }
    }catch (e) {
        console.log("verifyOtp sms", e);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    }
}

const GetAllUsers = (req, res, next) => {
    let recordsNo = parseInt(req.body.recordsPerPage);
    let pageNo = parseInt(req.body.pageNo);
    let start = recordsNo * (pageNo - 1);
    let limit = recordsNo;
    Models.User.aggregate([
        {
            $lookup: {
                from: "useractivities",
                localField: "id",
                foreignField: "user_id",
                as: "useractivitiesInfo"

            }
        },
        {$unwind: {path: "$useractivitiesInfo", preserveNullAndEmptyArrays: true}},
        {$unwind: {path: "$useractivitiesInfo.activity", preserveNullAndEmptyArrays: true}},

        {
            $group: {
                _id: "$id",

                user_id: {"$first": "$id"},
                name: {"$first": "$name"},
                email: {"$first": "$email"},
                phone: {"$first": "$phone"},
                linkedin_profile: {"$first": "$linkedin_profile"},
                sign_in_method: {"$first": "$sign_in_method"},
                interest: {"$first": "$interests"},
                skills: {"$first": "$skills"},
                saved_items: {
                    $push: {
                        $cond: {
                            if: {$eq: ['$useractivitiesInfo.activity.activity_info.saved', true]},
                            then: '$useractivitiesInfo.activity.item_id',
                            else: "$$REMOVE"
                        }
                    }
                },
            }
        },
        {$skip: start},
        {$limit: limit},


        {
            $project: {
                user_id: 1,
                profile_data: {
                    name: {$cond: {if: "$name", then: "$name", else: "john doe"}},
                    //name:"$name",
                    email: {$cond: {if: "$email", then: "$email", else: ""}},
                    phone: {$cond: {if: "$phone", then: "$phone", else: ""}},
                    linkedin_profile: {$cond: {if: "$linkedin_profile", then: "$linkedin_profile", else: ""}},
                    sign_in_method: "$sign_in_method",
                    about: "demo about",
                    total_exp: "3",
                    interest: "$interest",
                    saved_items: "$saved_items",
                    experience: [
                        {
                            company_name: "demo company name",
                            role_desc: "demo role description",
                            start_date: "29/09/21",
                            end_date: "23/09/22",
                        },
                    ],
                    skills: "$skills",
                },

                device_data: [
                    {
                        device_id: "1234",
                        manufacturer: "apple",
                        os_ver: "apple1",
                        app_ver: "er3432",
                    },
                ],

            },

        },
    ]).exec(async function (err, userList) {
        if (err) {
            console.log("error--", err);
            Logger.error(`Error getting data for user profile`);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        } else if (!userList) {
            return next(setError(MSG.DATA_NOT_FOUND));
        } else if (userList) {
            Logger.logInfo(`Successfully got user profile data`);
            return res.send({data: userList, message: MSG.DATA_FOUND});
        }
    });

};

const GetActiveUsers = (req, res, next) => {
    const {user} = req;
    const userId = user.user;
    console.log("userId from auth---->>>", userId);
    Models.User.find({is_active: true, _id: {$ne: userId}}).sort({'name': 1})
        .then((userList) => {
            if (!userList) {
                return next(setError(MSG.DATA_NOT_FOUND));
            } else {
                return res.send({data: userList, message: MSG.DATA_FOUND});
            }
        })
        .catch((err) => {
            console.log("User list err: ", err);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        });
};

const deleteUsers = async (req, res, next) => {
    try {

        Models.User.deleteMany(
            // { email: req.body.email,phone:req.body.phone },
            ({$or: [{email: req.body.email}, {phone: req.body.phone}, {update24hrsTime: req.body.update24hrsTime}]}),

            (err, userData) => {
                if (err) {
                    console.log("Update user err: ", err);
                    return next(setError(MSG.INTERNAL_ERROR, 500));
                } else if (userData.length === 0) {
                    return next(setError(MSG.DATA_NOT_FOUND));
                } else {
                    return res.send({data: userData, message: MSG.SUCCESS});
                }
            }
        );
    } catch (error) {
        return res.status(500).json({success: false, error: error});
    }
};

const GetRecentUpdatedUsers = async (req, res, next) => {
    const {user} = req;
    const userId = user.user;
    let  { datetime } = req.body;
    try {


        let dbUser = await Models.User.findOne({_id: ObjectId(userId)}, {recent_seen_time: 1});
        if (dbUser && dbUser.recent_seen_time) {
            datetime = dbUser.recent_seen_time;
        }
        let userList = await Models.User.aggregate([
            {
                $match: {
                    updatedAt: {$gt: new Date(datetime)},
                },
            },
            {
                $project: {
                    user_id: "$_id",
                    name: "$name",
                    email: "$email",
                    phone: "$phone",
                    linkedin_profile: "$linkedin_profile",
                    sign_in_method: "$sign_in_method",
                    about: "demo about",
                    total_exp: "3",
                    interest: "$interests",
                    skills: "$skills",
                },
            },
        ]);
        const currentDateTime= new Date();
        await Models.User.updateOne({_id: ObjectId(userId)}, {recent_seen_time: currentDateTime});
        userList.push({currentDateTime: currentDateTime});
        console.log("usersList--->>>", userList);
        if (!userList) {
            return next(setError(MSG.DATA_NOT_FOUND));
        } else {
            Logger.logInfo(`Error getting data for user :"${userId}"`);
            return res.send({data: userList, message: MSG.DATA_FOUND});
        }
    }catch (e) {
        Logger.error(`Error getting recent updated data for user :"${userId}"`);
        console.log("error-->>", err);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    }
};

const Login = (req, res, next) => {
    console.log("here inside login");
    const {email:emailParam, password} = req.body;
    Models.User.findOne({
        email: emailParam,
    })
        .then((user) => {
            if (!user) {
                return next(setError(MSG.LOGIN_INVALID, 401));
            } else {
                user.isCorrectPassword(password, function (err, same) {
                    if (err) {
                        return next(setError(MSG.PASSWORD_NOT_GENRATE));
                    } else if (!same) {
                        return next(setError(MSG.LOGIN_INVALID, 401));
                    } else {
                        let userInfo = user.toJSON();
                        delete userInfo.password;
                        let {_id, email, name, id} = userInfo;
                        const payload = {email, _id, name, id};
                        const token = auth.getToken(payload);
                        userInfo.token = token;
                        res.cookie("token", token, {httpOnly: true}).send({
                            data: userInfo,
                            message: MSG.LOGIN_SUCCESS,
                        });
                    }
                });
            }
        })
        .catch((err) => {
            console.log("User list err: ", err);
            return next(setError(MSG.INTERNAL_ERROR, 500));
        });
};

const getToken = (req, res) => {
    const {user} = req;
    Models.User.findOneAndUpdate({_id:user.user},{$set:{last_login_time: new Date()}},{ new: true}, (err, dbuser) => {
        if (dbuser && !err) {
            const token = auth.getToken({user: dbuser._id, id: dbuser.id});
            return res.send({
                data: dbuser,
                token: token,
                message: MSG.REGISTER_SUCCESS,
            });
        }
    })
};

const getShareFeedUserList = (req, res, next) => {
    Models.User.aggregate([
        {
            $lookup: {
                from: "chatrooms",
                let: {user_id: "$id"},
                pipeline: [
                    {
                        $match: {
                            $expr: {
                                $and: [


                                    {$in: ["$$user_id", "$id"]},
                                    {$in: [parseInt(req.body.id), "$id"]}

                                ]
                            }
                        }
                    }
                ],
                as: "users"
            }
        },
        {$unwind: "$users"},
        {
            $match: {
                id: {$ne: parseInt(req.body.id)}
            }
        },
        {$sort: {name: 1}},
        {
            $project: {
                _id: 1,
                name: 1,
                image: 1,
                id: 1
            }
        }
    ]).exec(function (err, userData) {
        if (err) {
            Logger.error(`Error getting data for user :"${req.body.id}"`);
            console.log("error-->>", error);

        } else {
            Models.User.find({id: {$ne: req.body.id}}).sort({'name': 1})
                .then((userList) => {
                    if (!userList) {
                        return next(setError(MSG.DATA_NOT_FOUND));
                    } else {
                        Logger.logInfo(`Success getting data for user :"${req.body.id}"`);
                        return res.send({
                            allUserList: userList,
                            recentContactedUserList: userData,
                            message: MSG.DATA_FOUND
                        });
                    }
                })
        }
    })
}

const getUserInfo = async (req, res,next) => {
    const {contacts = [], emails = []} = req.body;
    try {
        const users = await Models.User.aggregate([
            {
                $addFields: {
                    phone1: {$cond:[{$gt:[{ "$strLenCP": "$phone" },10]},{
                            "$substr": ["$phone", {
                                "$subtract": [
                                    { "$strLenCP": "$phone" },
                                    10
                                ]
                            },
                                { "$strLenCP": "$phone" }]
                        },"$phone"
                        ]}
                }
            },
            {$match:{ $or:[{phone:{$in: contacts}}, { email:{ $in : emails}}, {phone1:{$in: contacts}}]}},
            {
                $project:{
                    _id:1,
                    id:1
                }
            }
        ])
       if(users && users.length > 0){
           return res.send({
               user: users[0],
               message: MSG.DATA_FOUND
           });
       }else{
           return next(setError(MSG.DATA_NOT_FOUND));
       }
    } catch (e) {
        return next(setError(e));
    }
}
const sendInvite = async (req, res,next) => {
    const {user} = req;
    const contacts = req.body;
    try {

        for await (const contact of contacts) {

           let param = { ...contact, user_name : user.name};
            if (!user && contact.phone) {
                await Models.SystemAlert.send(param,"0001")
                // send sms
            } else if (contact.email) {
                await Models.SystemAlert.send(param,"0002")
                // send email
            }
        }
        return res.send({
            message: MSG.SUCCESS
        });
    }catch (e) {
        return next(setError(e));
    }
}
module.exports = {
    SocialMediaRegister,
    RegisterWithPhone,
    Register,
    UpdateRegisteredUser,
    GetUsers,
    TwoStepAuthentication,
    sendOtp,
    GetAllUsers,
    GetActiveUsers,
    Login,
    GetRecentUpdatedUsers,
    getToken,
    verifyOtp,
    getShareFeedUserList,
    generateRegistrationToken,
    deleteUsers,
    getUserInfo,
    sendInvite

};
