from app import create_app
import conf

application = create_app('config.DevelopmentConfig')

from flask_socketio import SocketIO,emit
socketio = SocketIO(application)
@socketio.on('my event') 
def test_message(message):
  emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
  application.run(host='0.0.0.0', port=4040)