import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Adjusting the system path to import the TaskWeaver library
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import TaskWeaver functions
from tw_backend.TaskWeaverasLibrary import initialize_taskweaver, get_response as taskweaver_get_response

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize TaskWeaver session
session = initialize_taskweaver()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    print(f"Received message: {user_input}")
    response = taskweaver_get_response(session, user_input)
    print(f"Response: {response}")
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)

    # debug=False to avoid the Flask server from restarting on every change
    # use_reloader=False to avoid the Flask server from restarting on every change

    # not sure if this is the best way to handle the Flask server, but it works for now
