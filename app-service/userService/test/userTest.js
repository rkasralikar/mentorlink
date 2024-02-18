const { ObjectId } = require('bson');
const random = require('randomatic');
const app = require('../app');
const chai = require('chai');
const chaiHttp = require('chai-http');
const should = chai.should();

chai.use(chaiHttp);
let id = () => ObjectId(random('0a', 12).toString('hex'));
var updateId = '';
var registrationToken ='eyJhbGciOiJIUzI1NiJ9.bWVudG9ybGlua1VzZXJQYXlsb2Fk.dLPhI87FoxgdVX8k4Ar8z9ZA3tbz3J_-bcqJm9iLrVE';

let socialMediaData = {
    userid: id(),
    name: `${random('a', 6)} ${random('a', 6)}`,
    email: `${random('a0', 10)}@yopmail.com`,
    is_deleted: 1,
    image: '',
    sign_in_method: 'social-media',
    skills: [id()],
    interests: [id()],
    career_summary: 'Developer.',
    term_accepted: 1,
    event: 'event',
    category: 'register_with_social_media',
    action: 'registration',
    label: 'Register user by social media.',
    value: '1'
};

let userUpdateData = {
    userid: id(),
    name: `${random('a', 6)} ${random('a', 6)}`,
    email: `${random('a0', 10)}@yopmail.com`,
    is_deleted: 1,
    image: '',
    skills: [id()],
  //  interests: [id()],
    career_summary: 'updated data',
    term_accepted: 1,
    event: 'event',
    category: 'update-user-after-registration',
    action: 'update_user',
    label: 'Update user after registration.',
    value: '1',
   
};

let phoneRegisterData = {
    name: `${random('a', 6)} ${random('a', 6)}`,
    phone: `${random('0', 10)}`,
    sign_in_method: `phone`,
    skills: [id()],
    interests: [id(), id()],
    career_summary: random('a ', 20),
    term_accepted: 1,
    is_deleted: 1,
    event: 'event',
    category: 'register_with_phone',
    action: 'registration',
    label: 'Register user by phone.',
    value: '10'
};

let getAllProfiles = {
    pageNo : '1',
    recordsPerPage : '10'
}

let getShareFeedUserList = {
    id : 584
}





describe('User registration with social media', ()=>{
    it('should register user with social media', (done) => {
        chai.request(app)
            .post('/users/register-with-social-media')
            .set('x-access-token', `${registrationToken}`)
            .send(socialMediaData)
            .end((err,res)=>{
                // console.log ("res",res)
                // console.log("err",err);
              
                token = res.body.token
                console.log("token from refister----->>>",token)
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                updateId = res.body.data
                console.log("User social media test response Body: ", res.body.message);
                // console.log (result);
                done();
                
            });
    });
});


describe('User registration using phone', ()=>{
    it('should user data for register', (done) => {
        chai.request(app)
            .post('/users/register-with-phone')
            .set('x-access-token', `${registrationToken}`)
            .send(phoneRegisterData)
            .end((err,res)=>{
                //console.log (res)
                // console.log("err",err);
                res.should.have.status(200);
                console.log("User social media test response Body: ", res.body.message);
                // console.log (result);
                done();
            });
    });
});




describe('User update information after registration', ()=>{
    it('should user data to update after registration', (done) => {
        console.log("token before update api-->>>.",token)
       
        chai.request(app)
            .post('/users/update-user-information/')
            .set('x-access-token', `${token}`)
            .send(userUpdateData)
            .end((err,res)=>{
                //console.log (res)
                console.log("err",err);
                res.should.have.status(200);
            //    console.log("User updated data after registration: ", res.body);
                // console.log (result);
                done();
            });
    });
});

describe('Retrieve User Information by Id', ()=>{
    it('should get registered user data by Id', (done) => {
        chai.request(app)
            .get('/users/profile/')
            .set('x-access-token', `${token}`)
            .end((err,res)=>{
                //console.log (res)
                // console.log("err",err);
                res.should.have.status(200);
                console.log("User updated data after registration: ", res.body.message);
                // console.log (result);
                done();
            });
    });
});


describe('Retrieve All Users', ()=>{
    it('should get all the users ', (done) => {
        chai.request(app)
            .post('/users/allprofiles/')
            .send(getAllProfiles)
            .set('x-access-token', `${token}`)
            .end((err,res)=>{
                //console.log (res)
                // console.log("err",err);
                res.should.have.status(200);
                console.log("Got all the users profile: ", res.body.message);
                // console.log (result);
                done();
            });
    });
});

describe('Retrieve All Active Users', ()=>{
    it('should get all the  active users ', (done) => {
        chai.request(app)
            .get('/users/getUsersList/')
            .set('x-access-token', `${token}`)
            .end((err,res)=>{
                //console.log (res)
                // console.log("err",err);
                res.should.have.status(200);
                console.log("Got all the active  users profile: ", res.body.message);
                // console.log (result);
                done();
            });
    });
});

describe('delete specified users', ()=>{
    console.log("deleteData-->>",deleteData)
    it('delete specified users ', (done) => {
        chai.request(app)
            .delete('/users/deleteUsers/')
            .send(deleteData)
            .end((err,res)=>{
                //console.log (res)
                // console.log("err",err);
                res.should.have.status(200);
                console.log("Delete Speicifed Users: ", res.body.message);
                // console.log (result);
                done();
            });
    });
});







