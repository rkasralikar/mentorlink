const { ObjectId } = require('bson');
const random = require('randomatic');
const app = require('../app');
const chai = require('chai');
const chaiHttp = require('chai-http');
const should = chai.should();

chai.use(chaiHttp);
let id = () => ObjectId(random('0a', 12).toString('hex'));
roomId = "ece2bcceca134d95b8ab46975eab5f4f"
var updateId = '';
var token ='';

let initiateChatData = {
    userIds:["60c71d1e973c439587280864","60c71d1e973c439587280860"],
    type:"consumer to consumer"
};

describe('Initiate a Chat Room', ()=>{
    it(' create a chat room for users', (done) => {
        chai.request(app)
            .post('/chats/initiate/')
            .send(initiateChatData)
            .end((err,res)=>{
             console.log("err--->>",err)   
                res.should.have.status(200);
                chai.expect(res.body).to.contain.property("message");
              
                updateId = res.body.data
                console.log("Initiate Chat Room response Body: ", res.body.message);
                // console.log (result);
                done();
                
            });
    });
});