import sys, os
import cgitb
import json

def init(handle_errors=True):
    if handle_errors:
        cgitb.enable()

def getarray():
    # Setup get and post arrays
    GET={}
    args=os.getenv("QUERY_STRING").split('&')

    for arg in args: 
        if '=' in arg:
            t=arg.partition('=')
            GET[t[0]]=t[2]
    return GET

def postarray():
    POST={}
    args=sys.stdin.read().split('&')

    for arg in args: 
        if '=' in arg:
            t=arg.partition('=')
            POST[t[0]]=t[2]
    return POST

def get_environment():
    env = {}
    keys = os.environ.keys()
    keys.sort()
    for k in keys:
        env[k] = os.environ[k]
    return env

def output_json(d,pretty=True):
    print "Content-type: application/json"
    print
    if pretty:
        print json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        print json.dumps(d)
