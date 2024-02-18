const { Kafka } = require('kafkajs');
const fs = require("fs");
const { SERVER_IPS, USERNAME, PASSWORD, CERT } =Config.get('Kafka');
let kafkaConfig = {
    clientId: 'app-service',
    requestTimeout: 25000,
    connectionTimeout: 3000,
    brokers: SERVER_IPS,
}
if(CERT){
    kafkaConfig.ssl= {
        ca: [fs.readFileSync('./kafka/ca.pem', 'utf-8')],
    };
}
if(USERNAME && PASSWORD){
    kafkaConfig.ssl= true;
    kafkaConfig.sasl= {
        mechanism: 'scram-sha-512', // scram-sha-256 or scram-sha-512
        username: USERNAME,
        password: PASSWORD
    }
}

const kafka = new Kafka(kafkaConfig);
const producer = kafka.producer();

(async () => {
    try {
        await producer.connect();
    } catch (e) {
        console.error(e)
    }
})();
const send = async (topic, message)=> {
    await producer.send({
        topic: topic,
        messages: [
            { value: JSON.stringify(message) },
        ],
    })
}
module.exports = {
    send
}