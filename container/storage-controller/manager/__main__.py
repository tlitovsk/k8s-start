from bottle import Bottle, request, response, HTTPResponse
from volume_manager import VolumeWorker
import json

app = Bottle()


@app.error(405)
def method_not_allowed(res):
    print("Method Not Allowed")
    if request.method == 'OPTIONS':
        new_res = HTTPResponse()
        new_res.set_header('Access-Control-Allow-Origin', '*')
        new_res.set_header(
            'Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
        return new_res
    res.headers['Allow'] += ', OPTIONS'
    return request.app.default_error_handler(res)


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.route('/v1/version')
def version():
    return {"version": "v1.0", "service-name": "volume manager"}


@app.route('/v1/status')
def status():
    return {"status": "ready"}


@app.route('/v1/volumes/<volume>/<name>', method='POST')
def create(volume, name):
    data = json.loads(request.body.read().decode("utf8"))
    size = data.get('size')
    volume_worker = VolumeWorker(volume)
    return volume_worker.add_disk(name, size)


@app.route('/v1/volumes/<volume>/<name>', method='DELETE')
def delete(volume, name):
    volume_worker = VolumeWorker(volume)
    return volume_worker.delete_disk(name)


@app.route('/v1/volumes/<volume>/', method='GET')
def list(volume):
    volume_worker = VolumeWorker(volume)
    return volume_worker.list_disks()


@app.route('/v1/volumes', method='GET')
def volumes():
    return {"volumes": [{"name": "nfs"}]}


app.run(host='0.0.0.0', port=8084, debug=True, reloader=True)
