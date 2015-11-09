'''
.. module:: alt_text_grabber
    :platform: Linux
    :synopsis: This file contains library functions for dealing with a uploaded 
    text file. It takes each line and encrypts it. The goal is returning 
    a new encrypted, text file for uploading to Google. 
    
.. moduleauthor:: Scott D.
'''

import os, shutil
import hashlib
import datetime as dt


def handle_uploaded_email_f(media_root, f):
    '''Takes a  file uploaded in a Post form, an copies it into
    the media folder 
    
    :param media_root: the Django media root directory.
    :type media_root: str.
    :param f: the file  uploaded.
    :type f: File object 
    :return resp: info about the HTML files found in the file.
    :rtype: dict.'''
    resp = {'result': ''}
    encr_emails = []
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    #full_path = media_root + '/' + f.name
    dest_dir = os.path.join(media_root,  'job_' + now_sfx)
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
    try: 
        plain_emails = f.readlines()
        
        for plain_email in plain_emails:
            hash_obj = hashlib.sha256(plain_email.strip())
            encr_emails.append(hash_obj.hexdigest())
                        
        f = open(dest_dir + '/encrypted_emails.csv', 'wb')
        f.write('\n'.join(encr_emails))
        f.close()
         
        
        resp['result'] = 'File {} created'.format(dest_dir + '/encrypted_emails.csv')
        resp['link_dir'] =  'job_' + now_sfx                
  
    except Exception as exc:
        resp['result'] = 'There was a problem: ' + exc.__str__() 
    return resp
    
    
