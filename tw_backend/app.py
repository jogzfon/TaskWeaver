import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from TaskWeaverasLibrary import initialize_taskweaver, get_response as taskweaver_get_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
session = initialize_taskweaver()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    response = taskweaver_get_response(session, user_input)
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)