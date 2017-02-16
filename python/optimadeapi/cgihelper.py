#!/usr/bin/env python
#
# This file is part of the optimadeapi project, which is covered by the MIT License
# Details are given in the LICENSE file in the root of this project.
# (c) Rickard Armiento, 2016-2017

import sys, os
import cgitb
import json
import urllib2

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

def input_json(jsonstr):
    return json.loads(jsonstr)

def comma_separated_to_list(s):
    return s.split(",")

def make_get_request(url,headers={}):
    request = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(request).read()
    
    
    
