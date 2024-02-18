const { ObjectId } = require('bson');
const random = require('randomatic');
const app = require('../app');
const chai = require('chai');
const chaiHttp = require('chai-http');
const should = chai.should();
var updateId = '';
var feedId ;
 let token ='';
chai.use(chaiHttp);
let id = () => ObjectId(random('0a', 12).toString('hex'));

let token1 ='';

let likeFeedData = {
    like_info:[{
        isLiked:"1",
          }]
};

let dislikeFeedData = {
    dislike_info:[{
        isDisliked:"1",
               }]
};

let saveFeedData = {
    save_info:[{
        isSaved:"",
      

        }]
};

let allProfileData = {
    pageNo : ' 1',
   recordsPerPage : ' 3' 
};

let getFeedData = {
    interests : ["Javascript"]
}


/*describe('Feed Get information', ()=>{
    it('should get feeds information', (done) => {
        chai.request(app)
            .post('/feeds/')
            .set('x-access-token', `${token}`)
            .send(getFeedData)
            .end((err,res)=>{
                // console.log ("res",res)
                // console.log("err",err);
              
              
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                feedId = res.body.data[0].item_id
                console.log("Feed get Data: ", res.body.data[0].item_id);
                // console.log (result);
                done();
                
            });
    });
});
describe('Feed Update like information', ()=>{
    it('should update like information', (done) => {
        chai.request(app)
            .post('/feeds/update-like-information/'+feedId)
            .set('x-access-token', `${token}`)
            .send(likeFeedData)
            .end((err,res)=>{
                // console.log ("res",res)
                // console.log("err",err);
              
              
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                updateId = res.body.data
                console.log("Feed like works: ", res.body.message);
                // console.log (result);
                done();
                
            });
    });
});

describe('Feed Update dislike information', ()=>{
    it('should update dislike information', (done) => {
        chai.request(app)
            .post('/feeds/update-dislike-information/'+feedId)
            .set('x-access-token', `${token1}`)
            .send(dislikeFeedData)
            .end((err,res)=>{
                // console.log ("res",res)
                // console.log("err",err);
              
               
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                updateId = res.body.data
                console.log("Feed dislike works: ", res.body.message);
                // console.log (result);
                done();
                
            });
    });
});

describe('Feed Update save  information', ()=>{
    it('should update save information', (done) => {
        chai.request(app)
            .post('/feeds/update-save-information/'+feedId)
            .set('x-access-token', `${token1}`)
            .send(saveFeedData)
            .end((err,res)=>{
                // console.log ("res",res)
                // console.log("err",err);
              
               
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                updateId = res.body.data
                console.log("Feed dislike works: ", res.body.message);
                // console.log (result);
                done();
                
            });
    });
});

describe('Feed Update visit  information', ()=>{
    it('should update visit information', (done) => {
        chai.request(app)
            .post('/feeds/update-visit-information/'+feedId)
            .set('x-access-token', `${token}`)
             .end((err,res)=>{
                // console.log ("res",res)
                // console.log("err",err);
              
               
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                updateId = res.body.data
                console.log("Feed visit works: ", res.body.message);
                // console.log (result);
                done();
                
            });
    });
});

describe('Feed get all user activites', ()=>{
    it('should update save information', (done) => {
        chai.request(app)
            .post('/feeds/alluseractivities/')
            .set('x-access-token', `${token1}`)
            .send(allProfileData)
            .end((err,res)=>{
                // console.log ("res",res)
                // console.log("err",err);
              
               
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                updateId = res.body.data
                console.log("Feed all user activity works: ", res.body.message);
                // console.log (result);
                done();
                
            });
    });
});*/


// describe('User registration using phone', ()=>{
//     it('should user data for register', (done) => {
//         chai.request(app)
//             .post('/users/register-with-phone')
//             .send(phoneRegisterData)
//             .end((err,res)=>{
//                 //console.log (res)
//                 // console.log("err",err);
//                 res.should.have.status(200);
//                 console.log("User social media test response Body: ", res.body.message);
//                 // console.log (result);
//                 done();
//             });
//     });
// });




// describe('User update information after registration', ()=>{
//     it('should user data to update after registration', (done) => {
//         console.log("token before update api-->>>.",token)
       
//         chai.request(app)
//             .post('/users/update-user-information/')
//             .set('x-access-token', `${token}`)
//             .send(userUpdateData)
//             .end((err,res)=>{
//                 //console.log (res)
//                 console.log("err",err);
//                 res.should.have.status(200);
//             //    console.log("User updated data after registration: ", res.body);
//                 // console.log (result);
//                 done();
//             });
//     });
// });

// describe('Retrieve User Information by Id', ()=>{
//     it('should get registered user data by Id', (done) => {
//         chai.request(app)
//             .get('/users/profile/')
//             .set('x-access-token', `${token}`)
//             .end((err,res)=>{
//                 //console.log (res)
//                 // console.log("err",err);
//                 res.should.have.status(200);
//                 console.log("User updated data after registration: ", res.body.message);
//                 // console.log (result);
//                 done();
//             });
//     });
// });


// describe('Retrieve All Users', ()=>{
//     it('should get all the users ', (done) => {
//         chai.request(app)
//             .post('/users/allprofiles/')
//             .send(getAllProfiles)
//             .set('x-access-token', `${token}`)
//             .end((err,res)=>{
//                 //console.log (res)
//                 // console.log("err",err);
//                 res.should.have.status(200);
//                 console.log("Got all the users profile: ", res.body.message);
//                 // console.log (result);
//                 done();
//             });
//     });
// });

// describe('Retrieve All Active Users', ()=>{
//     it('should get all the  active users ', (done) => {
//         chai.request(app)
//             .get('/users/getUsersList/')
//             .set('x-access-token', `${token}`)
//             .end((err,res)=>{
//                 //console.log (res)
//                 // console.log("err",err);
//                 res.should.have.status(200);
//                 console.log("Got all the active  users profile: ", res.body.message);
//                 // console.log (result);
//                 done();
//             });
//     });
// });




