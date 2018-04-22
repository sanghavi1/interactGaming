var socket;

$(function() {
    var room_members = $('.room-members');
    var map = null;
    var userCenter = [];
    var markers = [];

    $(window).on('unload', function() {
        socket.emit('left', {});
    });

    socket = io();

    socket.on('connect', function() {
        socket.emit('joined', {});
    });

    socket.on('list of users', function(data) {
        room_members.empty();
        for (var i = 0; i < data.users.length; i++) {
            room_members.append('<li>' + data.users[i] + '</li>');
        }
    });

    socket.on('error', function(){
        window.location.href ='/';
        alert("Hey, I think you broke something. I'm bringing you back to the homepage.");
    });

    socket.on('allPlayersReady', function(){
        window.location.href = '/playGame'
    });
    
});

function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        window.location.href = '/';
    });
}

function ready() {
    $(document.body).append("<h1> Ready </h1>")
    socket.emit('ready', {}, function() {

    });
}