#!/usr/bin/env python
#
# This file is part of the optimadeapi project, which is covered by the MIT License
# Details are given in the LICENSE file in the root of this project.
# (c) Rickard Armiento, 2016
#
# This software is an implementation of the OPTIMADE minimal api for materials databases
# It maps an OPTIMADE minimal API query onto a materialsproject.org query
# We only implement the <baseurl>/all endpoint
# Other OPTIMADE minimal API endpoints can be provided via URL mapping onto this endpoint:
# 
# /info -> /all?_omdb_introspection=baseurl
# /x/info -> /all?entry=x&_omdb_introspection=entry + any added url parameters
# /x -> /all?entry=x + any added url parameters
# /x/y -> /all?entry=x&filter=id=y + any added url parameters
#
# Here is how to do it with apache rewrite rules:
# 
# RewriteEngine On
# RewriteRule ^/info$ /all?_omdb_introspection=baseurl [QSA,L]
# RewriteRule ^/([^/]*)/info$ /all?entry=$1&_omdb_introspection=entry [QSA,L]
# RewriteRule ^/([^/]*)/([^/]*)/?$ /all?entry=$1&filter=id=$2 [QSA,L]
# RewriteRule ^/([^/]*)$ /all?entry=$1 [QSA,L]
#

# TODO: Read this from config file
BASE_URL="http://minapi.openmaterialsdb.se/"
##

import os, sys, cgi, datetime
from cgi import escape
import cgihelper

### Get ags array from merge of GET and POST, with priority to POST

cgihelper.init()
args = cgihelper.getarray()
args.update(cgihelper.postarray())
serverargs = cgihelper.get_environment()

response = {'args':args,'query':{'api_version':1},'resource':{'base_url':BASE_URL,'_omdb_env':serverargs}}
data = []

### Assemble response

if '_omdb_introspection' in args and args['_omdb_introspection'] == 'baseurl':
    response['_omdb_query_type']="Baseurl introspection"
    data=[
  {
   "/structures": {
     "get": {
      "description": "Short description of property",
      "unit": "MPa",
      "produces": [
       "application/json"
      ],
      "responses": {
       "200": {
        "description": "successful operation"
       }
      }
    }
   }
  },
  {
    "/structures/{id}": {
    "get": {
     "description": "Find property by ID",
     "produces": [
      "application/json"
     ],
     "responses": {
      "200": {
       "description": "Successful operation"
      },
      "400": {
       "description": "Bad request, mis-typed URL"
      }
     }
    }
   }
  }]

elif '_omdb_introspection' in args and args['_omdb_introspection'] == 'entry':
    response['_omdb_query_type']="Entry introspection"

elif 'filter' in args and args['filter'] != '':
    response['_omdb_query_type']="Query with filter"

elif 'entry' in args and args['entry'] != '':
    response['_omdb_query_type']="Query without filter"

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

import os, sys
from cgi import escape
print "Python %s" % sys.version
