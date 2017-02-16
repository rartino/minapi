#!/usr/bin/env python
#
# This file is part of the optimadeapi project, which is covered by the MIT License
# Details are given in the LICENSE file in the root of this project.
# (c) Rickard Armiento, 2016-2017

from optimadeapi import cgihelper

def query_v1_list_all_mids(base_url,entry):
    result = cgihelper.make_get_request(base_url+entry+"//mids")
    return cgihelper.input_json(result)["response"]

def query_v1_get_id(base_url,entry,id,mapi_key):
    result = cgihelper.make_get_request(base_url+entry+"/"+id+"/vasp",headers={'X-API-KEY': mapi_key})
    return cgihelper.input_json(result)["response"][0]

def send_v2_query(mapi_key, mapi_query):
    return ["Should send mapi request here"]

