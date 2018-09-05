import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from problem_manager import ProblemManager

encs_problem = ProblemManager(os.path.join(os.getcwd(), 'encs'))

app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    input_ = request.get_json()['input']
    if not input_:
        return jsonify({'output': ''})
    output = encs_problem.translate(input_)
    return jsonify({'output': output})
