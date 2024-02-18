module.exports = {
  
    SocialMediaRegistration: {
        userid: 'required',
        email: 'required',
        sign_in_method: 'required',
        term_accepted: 'required'
    },

    RegisterWithPhone:{
        phone: 'required',
        sign_in_method: 'required',
        term_accepted: 'required'
    },

    EmailRegistration: {
        email: 'required',
        password: 'required',
        sign_in_method: 'required',
        term_accepted: 'required'
        
    },
    UserLogin: {
        email: 'required',
        password: 'required'
    },
   
};
