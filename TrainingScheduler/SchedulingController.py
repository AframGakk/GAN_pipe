from flask import Flask
from flask import request, abort, json, jsonify, g
from flask_expects_json import expects_json
from Services.MQService.MQService import MQService
from Services.AuthService.AuthService import AuthService

_mqService = MQService()
_authService = AuthService()

app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'version': {'type': 'number'},
        'sound_type': {'type': 'string'},
        'parameters': {'type': 'object'}
    },
    'required': ['version', 'sound_type', 'parameters']
}

# POST new job
@app.route('/admin/training/job', methods = ['POST'])
@expects_json(schema)
def job_request():
    # auth validation
    if not request.headers['authorization']:
        abort(403, 'Header missing authenticaiton key')

    if not _authService.authenticate(request.headers['authorization']):
        abort(403, 'Authentication key is invalid')

    if request.method == 'POST':
        try:
            data = g.data
        except Exception:
            msg = 'body is not json serializable'
            abort(400, msg)

        # Send to MQ
        _mqService.sendTrainingMessage(data)

        return json.dumps({ 'success': True })


@app.route('/', methods = ['GET'])
def status():
    return 'Running'


if __name__ == '__main__':
    app.run(debug=False, port=5007)
