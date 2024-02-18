const Twilio =  Config.Twilio;
const { AccountSID, AuthToken, ServiceID,From:from } = Twilio;
const client = require("twilio")(AccountSID, AuthToken);
const sendEmailOTP = async (params) =>{
   const  { email } = params;
   const { TemplateID, EmailFrom, FromName } = Twilio;
   return await client.verify.services(ServiceID)
        .verifications
        .create({
            channelConfiguration: {
                template_id: TemplateID,
                from: EmailFrom,
                from_name: FromName
            }, to: email, channel: 'email'
        });
}

const sendSMSOTP = async (params)=>{
    const { phone } = params
    return await client.verify.services(ServiceID)
        .verifications
        .create({to: phone, channel: 'sms'});
}

const verifyOTP = async (params)=>{
    const {code, verificationChannel } = params;
    return await  client.verify.services(ServiceID)
        .verificationChecks
        .create({to: verificationChannel, code: code});
}

const sendSMS = async (params) => {
  const { body, to } = params;
  return await client.messages.create({
      body,
      to,
      from
  });
}
module.exports = {
    sendEmailOTP,
    sendSMSOTP,
    verifyOTP,
    sendSMS
}