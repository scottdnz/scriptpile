'''
.. module:: alt_text_grabber
    :platform: Linux
    :synopsis: This file contains library functions for dealing with a uploaded 
    
    
.. moduleauthor:: Scott D.
'''


import os, sys, csv, shutil
from StringIO import StringIO
import datetime as dt

import requests
from PIL import Image


def get_col_headings(path_to_f, separator):
    ''' '''
    res = {}
    links_rows = []
    
    csvfile = open(path_to_f, 'r')
    rdr = csv.DictReader(csvfile, delimiter=separator)
    fieldnames = tuple(rdr.fieldnames)
    csvfile.close()
    return fieldnames


def handle_link_f(media_root, f, format):
    '''Takes a file uploaded in a Post form...
    
    :param media_root: the Django media root directory.
    :type media_root: str.
    :param f: the file uploaded.
    :type f: File object
    :return resp: info about the HTML files found in the zip file.
    :rtype: dict.'''
    resp = {'result': '', 'fieldnames': (), 'dest_dir': '', 'errors': [], 
    'full_path': [] }
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    dest_dir = os.path.join(media_root,  'job_' + now_sfx)
    full_path = os.path.join(dest_dir, f.name)
    os.mkdir(dest_dir)
    
    if format == 'pipe':
        separator = '|'
    elif format == 'csv':
        separator = ','
    
    try:
        with open(full_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        relative_media_dir = media_root.replace(
            '/var/www/html/py/django_projects/scriptpile','')
        resp['dest_dir'] = os.path.join(relative_media_dir,  'job_' + now_sfx)                 
        resp['result'] = 'File uploaded successfully'
        
        resp['fieldnames'] = get_col_headings(full_path, separator)     
    except Exception as exc:
        resp['errors'].append('There was a problem: ' + exc.__str__())
    resp['full_path'] = full_path
    resp['separator'] = separator
    return resp
    
    
def read_csv_file(path_to_f, separator, cols_to_check, prefix):
    links_rows = {}
    prefix_yes = False
    if len(prefix) > 0:
        prefix_yes = True
    for col in cols_to_check:
        links_rows[col] = {}
    
    csvfile = open(path_to_f, 'r')
    rdr = csv.DictReader(csvfile, delimiter=separator)
    for row in rdr:
        for col in cols_to_check:
            url = row[col]
            if not prefix_yes and not 'http' in url:
                continue
            if 'http' in url:
                url_to_check = url
            if prefix_yes:     
                url_to_check = '{}{}'.format(prefix, url)
            #Only store unique URLs
            if url_to_check not in links_rows[col].keys():
                blank_dic = {'resp_code': '',
                    'resp_type': '',
                    'thumb_name': ''}
                links_rows[col][url_to_check] = blank_dic

    return links_rows
    

def try_each_link(links_rows):    
    res = {'links_rows': {}, 'errors': []}
    for k, v in links_rows.items():
        #print("*****".format(k))
        try:
            for url_k, url_v in v.items():
                #print('....')
                resp = requests.get(url_k)
                links_rows[k][url_k]['resp_code'] = unicode(resp.status_code)
                links_rows[k][url_k]['resp_type'] = resp.headers["content-type"]
        except requests.exceptions.ConnectionError as exc:
            res['errors'].append(exc.__str__())
    res['links_rows'] = links_rows
    return res
