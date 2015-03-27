#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

#from apiclient.discovery import build


def get_api_keys(conn, project_lbl, api_lbl):
    """ """
    api_keys = {'project_key': '', 
                'project_lbl': project_lbl,
                'api_key': '',  
                'api_lbl': api_lbl
    }
    sql = 'select label, encrypted_val from secret where label in ("{}", "{}");'
    sql = sql.format(project_lbl, api_lbl)
    cur = conn.cursor()
    cur.execute(sql)
    
    row = cur.fetchone()
    if row[0] == project_lbl:
        api_keys['project_key'] = row[1]
    elif row[0] == api_lbl:
        api_keys['api_key'] = row[1]
    row = cur.fetchone()
    if row[0] == project_lbl:
        api_keys['project_key'] = row[1]
    elif row[0] == api_lbl:
        api_keys['api_key'] = row[1]
    return api_keys
    
    
def get_req_result_set(collection, start_val, info):
    results = []
    # Make an HTTP request object
    request = collection.list(q=info['search_text'],
        num=3, 
        start=start_val,
        cx=info['search_engine_id']
    )
    #print('Searching ...')
    response = request.execute()

    for wsite in response['items']:        
        wsite_dic = {'site_name': wsite['displayLink'],
        'url': wsite['formattedUrl'],
        'title': wsite['title'],
        'img': ''}
        # Get a link to a thumbnail image if there is one
        if 'pagemap' in wsite.keys():
            if 'cse_thumbnail' in wsite['pagemap'].keys():
                wsite_dic['img'] = wsite['pagemap']['cse_thumbnail'][0]['src']
        results.append(wsite_dic)
    return results
        
	
def search_google(info):
    """ """
    #results = []
    #service = build('customsearch', 'v1', developerKey=info['api_key'])
    #collection = service.cse()
    #for i in range(0, info['num_requests']):
        # This is the offset from the beginning to start getting the results from
    #    start_val = 1 + (i * 3)
        #results.append(get_req_result_set(collection, start_val, info))
    #    print("{} results returned".format((i + 1) * 3))
        #output = json.dumps(response, sort_keys=True, indent=2)     
        
    #print(results)
        

#    output = json.dumps(response, sort_keys=True, indent=2)