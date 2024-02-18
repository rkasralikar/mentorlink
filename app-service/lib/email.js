const sgMail = require('@sendgrid/mail')
const {SendgridAPIKey} = Config.SendGrid;
const { EmailFrom, FromName } = Config.Twilio;
sgMail.setApiKey(SendgridAPIKey);
const sendEmail = async (params)=>{
    params.from = EmailFrom;
    params.fromName = FromName;
    try {
        return await sgMail
            .send(params);
    }catch (e) {
        console.log(e);
    }

}
module.exports = {
    sendEmail
}