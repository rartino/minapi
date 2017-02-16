#!/usr/bin/env python
#
# This file is part of the optimadeapi project, which is covered by the MIT License
# Details are given in the LICENSE file in the root of this project.
# (c) Rickard Armiento, 2016-2017

import mapiquery

all_fields_structures = ["id", "modification_date","elements", "nelements","chemical_formula","formula_prototype"]
all_fields_calculations = ["id", "modification_date"]

def mid_to_entry(mid, fields, source_api_url,mapi_key):
    result = mapiquery.query_v1_get_id(source_api_url,"materials",mid,mapi_key)
    result = dict([('_omdb_mapi_'+x,y) for x,y in result.iteritems()])

    ## Translate internal entries to the defined ones
    result['modification_date'] = None
    if '_omdb_mapi_elements' in result: 
        result['elements'] = ",".join(result['_omdb_mapi_elements'])
    else:
        result['elements'] = None
    if '_omdb_mapi_nelements' in result: 
        result['nelements'] = result['_omdb_mapi_nelements']
    else:
        result['nelements'] = None
    #TODO: change/make sure the formulas being output are the right ones
    if '_omdb_mapi_pretty_formula' in result: 
        result['chemical_formula'] = result['_omdb_mapi_pretty_formula']
    else:
        result['chemical_formula'] = None
    result['formula_prototype'] = "[not implemented]"
    result['id'] = mid
    data = {}
    if fields != None:
        for field in fields:
            data[field] = result[field] if field in result else None
    else:
        data = result
    return data

def get_data(entry, filterstr, fields, source_api_url, mapi_key, max_entries=3):
    if entry == 'structures':
        if filterstr=="":
            mids = mapiquery.query_v1_list_all_mids(source_api_url,"materials")
            total_count = len(mids)
            data = [mid_to_entry(x, fields, source_api_url, mapi_key) for x in mids[:max_entries]]
            return {'data':data, 'data_returned':len(data), 'data_available':total_count}
        elif filterstr.startswith("id=") and not ' ' in filterstr:
            # Special important filterstr case that can be handled more efficiently
            data = [mid_to_entry(filterstr[3:],fields, source_api_url,mapi_key)]
            return {'data':data, 'data_returned':1, 'data_available':1}
        else:
            
            return {'data':[], 'data_returned':0, 'data_available':0}
    elif entry == 'calculations':
        if filterstr=="":
            mapiquery.query_v1_list_all_mids(source_api_url,"tasks")
        else:
            return {'data':[], 'data_returned':0, 'data_available':0}
    else:  
        raise Exception("Unknown entry type.")
