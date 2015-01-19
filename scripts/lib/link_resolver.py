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
    res = {}
    links_rows = []
    
    csvfile = open(path_to_f, 'r')
    rdr = csv.DictReader(csvfile, delimiter=separator)
    fieldnames = tuple(rdr.fieldnames)
    csvfile.close()
    return fieldnames


def handle_link_f(media_root, f, format):
    '''Takes a file  uploaded in a Post form, an unzips it into
    the media folder. It searches for all HTML files inside, then parses each 
    one to build a images_info dict containing alt text for each image. 
    
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
    return resp
    
