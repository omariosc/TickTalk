# Imports app
from app import app, socketio

# Runs application
if __name__ == '__main__':
  socketio.run(app, debug=True)