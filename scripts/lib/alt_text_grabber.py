'''
.. module:: alt_text_grabber
    :platform: Linux
    :synopsis: This file contains library functions for dealing with a uploaded 
    zip file container, and extracting the HTML file, images and alt text 
    information inside. The goal is then to create thumbnails of any images 
    bigger than a certain height, and display the information found in a web 
    page.
    
.. moduleauthor:: Scott D.
'''

import requests, os, zipfile
from bs4 import BeautifulSoup
import datetime as dt


def handle_uploaded_f(media_root, f):
    '''Takes a zip file container uploaded in a Post form, an unzips it into
    the media folder. It searches for all HTML files inside, then parses each 
    one to build a images_info dict containing alt text for each image. 
    
    :param media_root: the Django media root directory.
    :type media_root: str.
    :param f: the zip file container uploaded.
    :type f: File object (zip).
    :return resp: info about the HTML files found in the zip file.
    :rtype: dict.'''
    resp = {'result': '',
            'html_files': {}}
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    full_path = media_root + '/' + f.name
    dest_dir = os.path.join(media_root,  'job_' + now_sfx)
    try:
        with open(full_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        
        res = unzip_zip_arch(media_root, f.name, dest_dir)
        
        html_files = find_all_html_files(dest_dir)
        
        for html_f in html_files.keys():
            images_info = parse_file(html_files[html_f]['path'])
            html_files[html_f]['images'] = images_info
        
        resp['html_files'] = html_files
        relative_media_dir = media_root.replace(
            '/var/www/html/py/django_projects/scriptpile','')
        resp['dest_dir'] = os.path.join(relative_media_dir,  'job_' + now_sfx)                 
       
    except Exception as exc:
        resp['result'] = 'There was a problem: ' + exc.__str__() 
    return resp


def unzip_zip_arch(media_dir, zf_name, dest_dir):
    '''Unzips a zipped file container (.zip format) and saves the extracted 
    files inside to a directory named like 'job_yyyymmdd_hhmmss'. 
    
    :param media_dir: the Django media root directory.
    :param zf_name: the zip file container name.
    :param dest_dir: the destination diretory for the extracted files.
    :return res: a confirmation message.
    '''
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    upload_z_file = os.path.join(media_dir, zf_name)
    
    os.mkdir(dest_dir)    
    with zipfile.ZipFile(upload_z_file, 'r') as z:
        z.extractall(dest_dir)
    res = 'Zip file "{}" unzipped to {}'.format(upload_z_file, dest_dir)
    os.remove(upload_z_file)
    return res


def find_all_html_files(job_dir):
    '''Examines files extracted in a job_x directory. 
    
    :param job_dir: the directory where extracted files wee stored.
    :return hml_files: information found in the HTML files.'''
    html_files = {}
    for f in os.listdir(job_dir):
        if '.htm' in f and '~' not in f:
            html_files[f] = {'path': os.path.join(job_dir, f),
                             'images': []}
    return html_files
    
    
def make_thumbnails(images_info, output_dir):
    '''
    '''
    size = (400, 100)
    os.mkdir(output_dir)
    
    for img in img_list:
        f = os.path.join(img_dir, img)
        fname = img[:img.rfind('.')] + '_thumb.jpg'     
        thumb_f = os.path.join(output_dir, fname)
        
        try:
            im = Image.open(f)
            (width, height) = im.size
            if height > 100:
                im.thumbnail(size)
                im.save(thumb_f, "JPEG")
                #images_info[]
            else:
                shutil.copy(f, output_dir)            
        except IOError as exc:
            res['errors'].append(
                'Cannot create thumbnail for {}. Error: {}'.format(img, 
                exc.__str__()))


# Functions for parsing HTML ##################################################
def parse_file(f_name):
    '''Processes all the img tags found in one HTML file. It then stores
    the alt and src property values.
    
    :param f_name: the HTML file path & name.
    :return info: information about each image found.
    :rtype info: dict.'''
    info = []
    soup = BeautifulSoup(open(f_name))
    images = soup.find_all('img')
    for img in images:
        info.append({'alt_text': img['alt'], 
                     'f_name': os.path.basename(img['src']),
                     'location': img['src'],
                     'orig_height': '',
                     'thumb_name': ''
                     })
    return info
