const chatService = require("../service/chatService");

module.exports = function (io) {

    let rooms = {};
    let allClients = [];
    io.on("connection", async function (socket) {
        Logger.log1("info","connected to socket io");
        await socket.emit("connected", {connected: "true"});

        Logger.log1("info","socket id---->>>"+ socket.id);


        socket.on("useronline", function (data) {

            const socketData = {
                userId: data.userId,
                socketId: socket.id
            }
            allClients.push(socketData);
            socket.emit("isonline", {online: true, userId: allClients});
            Logger.log1("info","users online-->>>", allClients);
        });

        socket.on('disconnect', function () {
            Logger.log1("info", 'Got disconnect!');
            Logger.log1("info", "disconnect socket id--->>> " + socket.id);
            if(rooms[socket.roomId]) {
                //let users = rooms[socket.roomId];
                //let i = users.indexOf(socket.id);
                //users.splice(i-1,i);
                //rooms[socket.roomId]= users;
            }
            Logger.log1("info","allClients array in disconnect--->>>", allClients)
            socket.emit("isonline", {online: true, userId: allClients});
        });

        socket.on("join room", roomID => {
            Logger.log1("info", "Join room fired"+ roomID);
            socket.roomId = roomID;
            if (rooms[roomID]) {
                Logger.log1("info", "Push")
                rooms[roomID].push(socket.id);
            } else {
                Logger.log1("info", roomID +" Created")
                rooms[roomID] = [socket.id];
            }
            socket.join(roomID);
            const otherUser = rooms[roomID].find(id => id !== socket.id);
            if (otherUser) {
                Logger.log1("info", "Other user fired and user joined fired")
                socket.emit("other user", otherUser);
                socket.to(roomID).emit("user joined", socket.id);
            }
        });

        socket.on("joinRoom", async function (data) {
          Logger.log1("info", "joinRoom--->>>" + data);
          await socket.join(data.chatRoomId);
          await socket.emit("onjoinroom", {data: data})
      });

        socket.on("leaveRoom", async function (data) {
            Logger.log1("info", "leaveRoomData--->>>" + data);
            await socket.leave(data.chatRoomId);
            await socket.emit("onleaveroom", {data: "leaved"})
        });

        socket.on('message', async function (data) {
            Logger.log1("info", "data before message emit---->>>"+ data)
            socket.to(data.chatRoomId).emit("chatmessage", {message: data});
            await chatService.postMessage(data);

        })


        socket.on('delievered', function (data) {
            Logger.log1("info", "delievered event---->>>"+ data);
            socket.emit('isdelievered', {message: "delievered", data: data})
        })

        socket.on('read', function (data) {
            Logger.log1("info", "read event---->>>"+ data);
            socket.emit('isread', {message: "read", data: data})
        })

        socket.on("offer", payload => {
            Logger.log1("info", "Offer fired "+ JSON.stringify(payload))
            socket.to(payload.target).emit("offer", payload);
        });

        socket.on("answer", payload => {
            Logger.log1("info", "Answer fired "+ JSON.stringify(payload))
            socket.to(payload.target).emit("answer", payload);
        });

        socket.on("ice-candidate", incoming => {
            Logger.log1("info", "Ice candidate fired "+JSON.stringify(incoming.candidate));
            socket.to(incoming.target).emit("ice-candidate", incoming.candidate);
        });

    });
};


