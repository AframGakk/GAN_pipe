from flask import Flask
from flask import request, abort, json, jsonify, g
from flask_expects_json import expects_json
from flask_cors import CORS, cross_origin
from Services.MQService.MQService import MQService
from Services.AuthService.AuthService import AuthService
from Services.JobService.JobService import getAllJobs, getJobById


_mqService = MQService()
_authService = AuthService()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

schema = {
    'type': 'object',
    'properties': {
        'label': {'type': 'string'},
        'version': {'type': 'number'},
        'sound_type': {'type': 'number'},
        'parameters': {'type': 'object'}
    },
    'required': ['label', 'version', 'sound_type', 'parameters']
}

# POST new job
@app.route('/admin/training/job', methods = ['POST'])
@cross_origin()
@expects_json(schema)
def job_post_requests():
    # auth validation
    if 'Authorization' not in request.headers:
        abort(403, 'Header missing authenticaiton key')

    if not _authService.authenticate(request.headers['authorization']):
        abort(403, 'Authentication key is invalid')

    # POST new job
    if request.method == 'POST':
        try:
            data = g.data
        except Exception:
            msg = 'body is not json serializable'
            abort(400, msg)

        # Send to MQ
        _mqService.sendTrainingMessage(data)

        return json.dumps({ 'success': True })


@app.route('/admin/training/job', methods = ['GET'])
@cross_origin()
def job_get_requests():
    # auth validation
    if 'Authorization' not in request.headers:
        abort(403, 'Header missing authenticaiton key')

    if not _authService.authenticate(request.headers['Authorization']):
        abort(403, 'Authentication key is invalid')

    # GET all jobs
    if request.method == 'GET':

        all_jobs = getAllJobs()

        return json.dumps({ 'success': True, 'data': all_jobs })


@app.route('/admin/training/job/<id>', methods = ['GET'])
@cross_origin()
def job_requests_item(id):
    # auth validation
    if 'Authorization' not in request.headers:
        abort(403, 'Header missing authenticaiton key')

    if not _authService.authenticate(request.headers['authorization']):
        abort(403, 'Authentication key is invalid')

    # GET all jobs
    if request.method == 'GET':

        job = getJobById(id)

        return json.dumps({ 'success': True, 'data': job })



@app.route('/healthcheck', methods = ['GET'])
@cross_origin()
def status():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5007)
