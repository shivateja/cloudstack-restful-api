from flask import Flask, request, abort
from api import apicall
from precache import apicache

app = Flask(__name__)

singular = {
        'events': 'event',
        'users': 'user',
        'accounts': 'account',
        'virtualmachines' : 'virtualmachine',
        'domains': 'domain'
        }

def get_args(multidict):
    """Default type of request.args or request.json is multidict. Converts it to dict so that can be passed to make_request"""
    data = {}
    for key in multidict.keys():
        data[key] = multidict.get(key)
    return data

@app.route('/api/<subject>', methods=['GET','POST'])
def collection(subject):
    """Operations on a collection of entities, list them or add an entity to collection"""
    if request.method == 'GET':
        args = get_args(request.args)
        verb = "list"
    if request.method == 'POST':
        args = get_args(request.json)
        verb = "create"
        subject = singular[subject];
    return apicall(verb, subject, args)

@app.route('/api/<subject>/<id>', methods=['GET', 'PUT', 'DELETE'])
def has_id(subject, id):
    """Operation on an entity with given id, list its properties, update its properties, delete it"""
    if request.method == 'GET':
        args = get_args(request.args)
        verb = "list"
        args["id"] = id
    if request.method == 'PUT':
        args = get_args(request.json)
        verb = "update"
        subject = singular[subject];
        args["id"] = id
    if request.method == 'DELETE':
        verb = "delete"
        subject = singular[subject];
    return apicall(verb, subject, args);

@app.route('/api/<parent>/<parent_id>/<children>', methods=['GET'])
def has_parent(parent, parent_id, children):
    """List the children of a given parent with its id"""
    args = get_args(request.args)
    if request.method == 'GET':
        #Something like /api/domains/<id>/virtualmachines will be equivalent to listVirtualMachines?domainid=<id>
        verb = "list"
        subject = children
        #If parent is 'domains' it is added into args as domainid, i.e singular[domains] + 'id'
        args[singular[parent] + 'id'] = parent_id
    return apicall(verb, subject, args)


#Verbs like start etc are to implemented here
#@app.route("/api/<subject>/<verb>")
#def verbandsubject(subject, verb):
#    command = get_command(subject, verb)
#    if command is None:
#        abort(404)
#    data = get_data(request.args)
#    response, error = make_request(command, data, None, host, port, apikey, secretkey, protocol, path)
#    if error is not None:
#        return error, get_error_code(error)
#    return response"""

if __name__ == '__main__':
    app.run(debug=True)
