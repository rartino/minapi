#!/usr/bin/env python
#
# This file is part of the optimadeapi project, which is covered by the MIT License
# Details are given in the LICENSE file in the root of this project.
# (c) Rickard Armiento, 2016-2017
#
# This software is an implementation of the OPTIMADE minimal api for materials databases
# It maps an OPTIMADE minimal API query onto a materialsproject.org query
# We only implement the <baseurl>/all endpoint
# Other OPTIMADE minimal API endpoints can be provided via URL mapping onto this endpoint:
# 
# /v1/ -> /
# /info -> /all?_omdb_introspection=baseurl
# /x/info -> /all?entry=x&_omdb_introspection=entry + any added url parameters
# /x -> /all?entry=x + any added url parameters
# /x/y -> /all?entry=x&filtering=id=y + any added url parameters
#
# Here is how to do it with apache rewrite rules:
# 
#        RewriteRule ^/favicon.ico /favicon.ico [L]
#        RewriteRule ^/v1/(.*) /$1?version=v1 [QSA]
#        RewriteRule ^/info$ /all?_omdb_introspection=baseurl [QSA,L]
#        RewriteRule ^/([^/]*)/info$ /all?entry=$1&_omdb_introspection=entry [QSA,L]
#        RewriteRule ^/([^/]*)/([^/]*)/?$ /all?entry=$1&filtering=id=$2 [QSA,L]
#        RewriteRule ^/([^/]*)$ /all?entry=$1 [QSA,L]

import os, sys, cgi, datetime
from cgi import escape
from ConfigParser import SafeConfigParser

import cgihelper
import baseurl_introspection
import entry_introspection
import filtering

config = SafeConfigParser()
config.read('optimade.ini')
base_url = config.get('main', 'base_url') 
source_database = config.get('main', 'source_database')
debug =  config.getboolean('main', 'debug')

cgihelper.init()
args = cgihelper.getarray()
args.update(cgihelper.postarray())
serverargs = cgihelper.get_environment()

request_uri=serverargs['REQUEST_URI']
representation = request_uri[request_uri.startswith(base_url) and len(base_url):]
if representation[0] != '/':
    representation = '/'+representation

response = {
    'query': {
        'api_version':'v1', 
        'representation':representation, 
        'data_returned':0
        },
    'resource':{
        'base_url':base_url,
        '_omdb_env':serverargs,
        '_omdb_cwd':os.getcwd(),
        '_omdb_args':args
        }
    }
data = []

### Deduce what type of query it is and assemble data

if '_omdb_introspection' in args and args['_omdb_introspection'] == 'baseurl':
    response['_omdb_query_type']="Baseurl introspection"
    try:
        data=baseurl_introspection.get_data(base_url, source_database, config)
    except Exception as e:
        #TODO: Handle errors accoding to spec
        data={'error': str(e)}
        if debug: raise

elif '_omdb_introspection' in args and args['_omdb_introspection'] == 'entry':
    response['_omdb_query_type']="Entry introspection"
    try:
        data=entry_introspection.get_data(args['entry'], source_database, config)
    except Exception as e:
        #TODO: Handle errors accoding to spec
        data={'error': str(e)}
        if debug: raise

elif 'filter' in args and args['filter'] != '':
    response['_omdb_query_type']="Query with filtering"
    try:
        fields = cgihelper.comma_separated_to_list(args['fields']) if 'fields' in args else None
        result=filtering.get_data(args['entry'], args['filter'], fields, source_database, config)
        data = result['data']
        response['query']['data_returned']=result['data_returned']
        response['query']['data_available']=result['data_available']
        
    except Exception as e:
        #TODO: Handle errors accoding to spec
        data={'error': repr(e)}
        if debug: raise

elif 'entry' in args and args['entry'] != '':
    response['_omdb_query_type']="Query without filtering"
    try:
        fields = cgihelper.comma_separated_to_list(args['fields']) if 'fields' in args else None
        result=filtering.get_data(args['entry'], "", fields, source_database, config)
        data = result['data']
        response['query']['data_returned']=result['data_returned']
        response['query']['data_available']=result['data_available']
        
    except Exception as e:
        #TODO: Handle errors accoding to spec
        data={'error': repr(e)}
        if debug: raise

response['data']=data

### Set timestamp to time when request is complete

response['query']['time_stamp'] = datetime.datetime.now().isoformat()

### Generate output

if '_omdb_prettyjson' in args and args['_omdb_prettyjson'] == 'false':
    cgihelper.output_json(response,pretty=False)
elif '_omdb_prettyjson' in args and args['_omdb_prettyjson'] == 'true':
    cgihelper.output_json(response,pretty=True)
else:
    cgihelper.output_json(response)

