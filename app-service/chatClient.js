var io = require("socket.io-client");
var socket = io.connect("http://localhost:8080", { reconnect: true });

// Add a connect listener
socket.on("connection", function (socket) {
  console.log("Connected!");
});

//socket.emit('joinRomm',)
socket.on("connected", async function (data) {
  console.log("connection with server done", data);
 await  socket.emit("joinRoom", { userId: "60bda84b79338d00126a999f" });

});

socket.on("onjoinroom", function (data) {
  console.log("room joined successfully", data);
    socket.emit("message",{chatRoomId:"60da1033dc287e0015ff1119",message:"updated message",postedByUser:"604c8b8caeb07256f07d3139",type:"image"})
});


socket.on("Shared", function (data) {
  console.log("inside share", data);
});


socket.on("chatmessage", function (data) {
  console.log("client received data", data);
});
