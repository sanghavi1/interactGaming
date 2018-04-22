from flask import session
from flask_socketio import emit, join_room, leave_room
from . import socketio
from app import rooms

@socketio.on('joined')
def joined(data):
    user = session['username']
    room = session['room_id']
    if room in rooms and user in rooms[room]['users']:
        emit('error')
    print '{} joined room {}'.format(user, room)
    join_room(room)
    if room not in rooms:
        rooms[room] = { 'users': {} }
    rooms[room]['users'][user] = {}
    rooms[room]['users'][user]['ready']="False"
    user_list = sorted(rooms[room]['users'].keys())
    emit('list of users', { 'users': user_list }, room=room)

@socketio.on('left')
def left(data):
    user = session['username']
    room = session['room_id']
    print '{} left room {}'.format(user, room)
    leave_room(room)

    if user in rooms[room]['users']:
        rooms[room]['users'].pop(user, None)

    user_list = sorted(rooms[room]['users'].keys())
    emit('list of users', { 'users': user_list }, room=room)

@socketio.on('ready')
def ready(data):
    user = session['username']
    room = session['room_id']

    rooms[room]['users'][user]['ready']="True";

    for x in rooms[room]['users']:
        if "False" in rooms[room]['users'][x]['ready']:
            return
    print "All Players are ready"

        