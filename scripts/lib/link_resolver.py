'''
.. module:: link_resolver
    :platform: Linux
    :synopsis: This file contains library functions for dealing with an uploaded 
    list of URLs, probably for images.
    
    
.. moduleauthor:: Scott D.
'''


import os, sys, csv, shutil
#from StringIO import StringIO
import datetime as dt

import requests
#from PIL import Image


def get_col_headings(path_to_f, separator):
    '''Returns a tuple of column names found in the first row of a datafile.
    
    :param path_to_f: the path to the datafile.
    :type path_to_f: str.
    :param separator: the delimiter character. 
    :type separator: str.
    :return fieldnames: all the column heading labels found in the datafile.
    :rtype: tuple.'''
    csvfile = open(path_to_f, 'r')
    rdr = csv.DictReader(csvfile, delimiter=separator)
    fieldnames = tuple(rdr.fieldnames)
    csvfile.close()
    return fieldnames


def handle_link_f(media_root, f, format):
    '''Takes a file uploaded in a Post form and writes it to the /media
    directory.
    
    :param media_root: the Django media root directory.
    :type media_root: str.
    :param f: the file uploaded.
    :type f: File object
    :param format: the delimiter format for the file.
    :type format: str.
    :return resp: info about the links in the selected file columns.
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
    '''Parses the datafile's selected column cells and stores in the information
    in a links_rows dict.
    
    :param path_to_f: the path to the uploaded data file.
    :type path_to_f: str.
    :param separator: the delimiter character.
    :type separator: str.
    :param cols_to_check: the selected column name labels to parse.
    :type cols_to_check: tuple.
    :param prefix: link text that should be inserted before the cell's text, e.g. 
    http://myserver/images/
    :type prefix: str.
    :return links_rows: information about the links found in each column.
    :rtype: dict.'''
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
            if len(url) == 0 or (not prefix_yes and not 'http' in url):
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
    '''Tries requesting each link associated with each nominated column's cells 
    in the datafile.
    
    :param links_rows: information about links found in the selected column 
    cells in the datafile.
    :type links_rows: dict.
    :return res: the results of trying each link found.
    :rtype: dict.'''
    res = {'links_rows': {}, 'errors': []}
    for k, v in links_rows.items():
        try:
            for url_k, url_v in v.items():
                resp = requests.get(url_k)
                links_rows[k][url_k]['resp_code'] = unicode(resp.status_code)
                links_rows[k][url_k]['resp_type'] = resp.headers["content-type"]
        except requests.exceptions.ConnectionError as exc:
            res['errors'].append(exc.__str__())
    res['links_rows'] = links_rows
    return res
