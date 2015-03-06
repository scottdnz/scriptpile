#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from apiclient.discovery import build


def get_api_keys(conn, project_lbl, api_lbl):
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
	
	
	
def search_google(info):
    results = []
    
    #output_f = open('res1.json', 'ab')    
    
    service = build('customsearch', 'v1', developerKey=info['api_key'])
    collection = service.cse()
    for i in range(0, info['num_requests']):
        # This is the offset from the beginning to start getting the results from
        start_val = 1 + (i * 10)
        # Make an HTTP request object
        request = collection.list(q=info['search_text'],
            num=3, 
            start=start_val,
            cx=info['search_engine_id']
        )
        print('Searching ...')
        response = request.execute()
        #output = json.dumps(response, sort_keys=True, indent=2)     
        #print(output)
     #   output_f.write(output)
    #output_f.close()
        for wsite in response['items']:        
            #for k, v in wsite.items():
#                print(k)
            wsite_dic = {'site_name': wsite['displayLink'],
            'url': wsite['formattedUrl'],
            'title': wsite['title'],
            'img': ''}
            if 'cse_thumbnail' in wsite['pagemap'].keys():
                wsite_dic['img'] = wsite['pagemap']['cse_thumbnail'][0]['src']
            results.append(wsite_dic)
    print(results)
        
        #"displayLink": "weddingwise.co.nz", 
        #"formattedUrl": "https://weddingwise.co.nz/vendor/natalie-shields",   
        #"title": "Natalie Shields Hairdresser & Makeup Artist : Beauty, Hair ..."
        #"cse_thumbnail": [
#          {
#            "height": "74", 
#            "src": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQ-s5HCMgVPAXI-fYKWnXXeUtW_zgOPETcU9tANpPhVjepaO_5iF4Ys", 
#            "width": "74"
#          }
#        ], 


    

#search_text, num_requests
#
#search_engine_id = '[My Search Engine ID]'
#api_key = '[My Project API Key]'
#collection = service.cse()
#for i in range(0, num_requests):
#    # This is the offset from the beginning to start getting the results from
#    start_val = 1 + (i * 10)
#    # Make an HTTP request object
#    request = collection.list(q=search_term,
#        num=10, #this is the maximum & default anyway
#        start=start_val,
#        cx=search_engine_id
#    )
#    response = request.execute()
#    output = json.dumps(response, sort_keys=True, indent=2)