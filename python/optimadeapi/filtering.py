#!/usr/bin/env python
#
# This file is part of the optimadeapi project, which is covered by the MIT License
# Details are given in the LICENSE file in the root of this project.
# (c) Rickard Armiento, 2016-2017
import re
import shlex

import optimadeapi.mapi.filtering

#def parse_filterstr(expression):
#    lexer = shlex.shlex(expression)
#    lexer.quotes = '"'
#    for token in lexer:
#        print repr(token)
#    #tokens = re.split('(AND|OR|NOT|<|<=|>|>=|=|!=)| +', filterstr)    
#    #terms = re.split("[ \t]",expression)

def get_data(entry, filterstr, fields, source_database, config):
    api_type = config.get(source_database, 'api_type')
    #if filterstr != "":
    #    filterdict = parse_filterstr(filterstr)    
    if api_type == 'mapi':
        source_api_url = config.get(source_database, 'api_url')
        mapi_key = config.get(source_database, 'mapi_key')
        return optimadeapi.mapi.filtering.get_data(entry, filterstr, fields, source_api_url, mapi_key)
    else:
        raise Exception("Unknown api type.")
