'use strict';
const Schema = Mongoose.Schema;
const SystemAlertSchema = Schema(
    {
        alert_id: String,
        business_trigger: String,
        text_body: String,
        subject: String,
        body: String,
        alert_type: String,
        sender_email: String,
        sender_name: String,
        cc: [String],
        cc_emails: [String],
        bcc: [String],
        bcc_emails: [String],
        to: [String],
        to_emails: [String],
        reply_to: String,
        status: {type: Boolean, default: true}
    },
    {
        timestamps: true,
        id: false,
        collection: 'system_alerts',
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
SystemAlertSchema.statics.send = async (data, alert) => {
    let alertData = alert;
    if (typeof alert === 'string') {
        alertData = await Models.SystemAlert.findOne({alert_id: alert});
    } else {
        alertData = alert ? alert.toObject() : {};
    }
    if (!empty(alertData) && alertData.status === true) {
        let alert = alertData.toObject();
        const { alert_id } = alert;
        switch (alert_id) {
            case '0001':
                let replacement = {
                    '[NAME]': data.name,
                    '[INVITE_USER_NAME]': data.user_name
                };
                alert.text_body = replaceMulti(alert.text_body, replacement);
                let smsParam = { body : alert.text_body, to: data.phone };
                 await  SMS.sendSMS(smsParam)
                break;
            case '0002':
                let replacement1 = {
                    '[NAME]': data.name,
                    '[INVITE_USER_NAME]': data.user_name
                };
                alert.body = replaceMulti(alert.body, replacement1);
                let param = { html : alert.body, to: data.email, subject:alert.subject };
                await EMAIL.sendEmail(param)
                break;
        }

    }
}
module.exports = Mongoose.model('SystemAlert', SystemAlertSchema);;