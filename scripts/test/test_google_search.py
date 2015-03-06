#!/usr/bin/env python


'''
'''

import os.path, sys
sys.path.append(os.path.abspath('../..'))

from scriptpile import settings
from scripts.lib.basic_db_access import (connect_to_db, decrypt_val)
from scripts.lib.google_search import *


if __name__ == '__main__':	
	res = connect_to_db(username=settings.DATABASES['default']['USER'], 
	password=settings.DATABASES['default']['PASSWORD'], 
	database=settings.DATABASES['default']['NAME'])
	
	project_lbl = 'custom search engine1'
	api_lbl = 'testSearch1 Project - api key'
	api_keys = get_api_keys(res['db_conn'], project_lbl, api_lbl)
	
	#print(api_keys)
	api_keys['project_key'] = decrypt_val(api_keys['project_key'], 
	   settings.ENCR_KEY, settings.ENCR_IV)
	api_keys['api_key'] = decrypt_val(api_keys['api_key'],
	   settings.ENCR_KEY, settings.ENCR_IV)
	
	
	info = {'search_text': 'Auckland Hairdresser',
    'num_requests': 1,
    'search_engine_id': api_keys['project_key'],
    'api_key': api_keys['api_key']
    }
        search_google(info)
    
        
    