from requester import make_request
from precache import apicache
from flask import Flask, request, abort

app = Flask(__name__)

apikey = "DNi_vTVLPNfTEFuqu5F9MrPI3iecf8iRQ3QtGUH1IM2Nd96wNwNlf7BzmF1W8aw6cE2ejZCgyE53wT5VpzauuA"
secretkey = "x4jM12uE4LNho3ZNJa8J-Ve6WsgEXd8df1mGGfeuJHMtolkaSBkD5pLX0tvj8YrWhBgtZbKgYsTB00kb7z_3BA"
path = '/client/api'
host = '10.6.1.253'
port = '8080'
protocol = 'http'

def get_command(subject, verb):
    commandlist = apicache.get(verb, None)
    if commandlist is not None:
        command = commandlist.get(subject, None)
        if command is not None:
            return command["name"]
    return None

def get_error_code(error):
    return int(error[11:14]) #Ugly

def get_data(multidict):
    """Default type(request.args) is multidict. Converts it dict that can be passed to make_request"""
    data = {}
    for key in multidict.keys():
        data[key] = multidict.get(key,"")
    return data

@app.route('/<subject>')
def onlysubject(subject):
    if request.method == 'GET':
        if subject in apicache["list"].keys():
            verb = "list"
            command = get_command(subject, verb)
        else:
            verb = "get"
            command = get_command(subject, verb)
    if request.method == 'POST':
        verb = "create"
        command = get_command(subject, verb)
    if request.method == 'PUT':
        verb = "update"
        command = get_command(subject, verb)
    if request.method == 'DELETE':
        verb = "delete"
        command = get_command(subject, verb)
    if command is None:
        abort(404)
    data = get_data(request.args)
    response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
    if error is not None:
        return error, get_error_code(error)
    return response

@app.route("/<subject>/<verb>")
def verbandsubject(subject, verb):
    command = get_command(subject, verb)
    if command is None:
        abort(404)
    data = get_data(request.args)
    response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
    if error is not None:
        return error, get_error_code(error)
    return response

if __name__ == '__main__':
    app.run(debug=True)
