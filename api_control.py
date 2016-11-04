from flask import Flask
from flask import request, json, Response, jsonify
import os

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Hello World'

@app.route('/move/<direction>', methods = ['POST'])
def move(direction):
    """Demand R4 to move into a directinon

    Response:
        status_code: 202 (Accepted) - The move request is accepted for processing
        (json): {
            move (str): The direction has just been requested
            result (str): Success sending request or not
        }
    """
    possible_directions = ['left', 'right', 'up', 'down']

    direction = direction.lower()
    if direction in possible_directions:
        # Trigger movement
        log = execute('echo "%s"' % direction)

        # Response
        resp = {
            'move': direction,
            'log': log,
            'result': 'success'
        }
        resp = jsonify(resp)
        resp.status_code = 202
        return resp
    else:
        return not_found()

@app.errorhandler(404)
def not_found():
    message = {
        'error': 'NOT FOUND'
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def execute(command):
    """Execute server os commands
    Return log's output
    """
    cmd = os.popen(command, "r").read()
    return cmd

if __name__ == '__main__':
    app.run(debug=True)
