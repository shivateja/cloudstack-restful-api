from requester import make_request
from flask import Flask, request, abort
from precache import apicache
import simplejson as json
import logging
from logging.handlers import RotatingFileHandler
import unicodedata

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
    return int(error[11:14])

@app.route('/<subject>')
def onlysubject(subject):
    if request.method == 'GET':
        if subject in apicache["list"].keys():
            verb = "list"
            command = get_command(subject, verb)
            if command is None:
                abort(404)
            data = dict(request.args) #Raising error 530 for some unknown issue if data is not empty
            response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
        else:
            verb = "get"
            command = get_command(subject, verb)
            if command is None:
                abort(404)
            data = dict(request.args)
            app.logger.info(str(data))
            response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
            app.logger.info(str(response))
        if error is not None:
            return error, get_error_code(error)
        return response
    if request.method == 'POST':
        verb = "create"
        command = get_command(subject, verb)
        if command is None:
            abort(404)
        data = dict(request.args)
        response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
        if error is not None:
            return error, get_error_code(error)
        return response
    if request.method == 'PUT':
        verb = "update"
        command = get_command(subject, verb)
        if command is None:
            abort(404)
        data = dict(request.args)
        response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
        if error is not None:
            return error, get_error_code(error)
        return response

    if request.method == 'DELETE':
        verb = "delete"
        command = get_command(subject, verb)
        if command is None:
            abort(404)
        data = dict(request.args)
        response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
        if error is not None:
           abort(get_error_code(error))
        return response

@app.route("/<subject>/<verb>")
def verbandsubject(subject, verb):
    command = get_command(subject, verb)
    if command is None:
        abort(404)
    data = dict(request.args)
    response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
    if error is not None:
        return error, get_error_code(error)
    else:
        return response

if __name__ == '__main__':
    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
