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

import os, zipfile, shutil
import datetime as dt
from StringIO import StringIO

#import requests
from bs4 import BeautifulSoup
from PIL import Image
import requests


def remove_bad_chars(thumb_fname):
    thumb_fname = thumb_fname.replace('?', '')
    thumb_fname = thumb_fname.replace('=', '')
    return thumb_fname


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
        #Copy the zip file container
        with open(full_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        #Extract the files inside
        res = unzip_zip_arch(media_root, f.name, dest_dir)
        #Find each HTML file and parse it for images information.
        html_files = find_all_html_files(dest_dir)
        for html_f in html_files.keys():
            images_info = parse_file(html_files[html_f]['path'])
            html_files[html_f]['images'] = images_info
        #Create thumbnails from the images
        thumbs_dir = os.path.join(dest_dir, 'thumbs')
        if os.path.isdir(thumbs_dir):
            shutil.rmtree(thumbs_dir)
        
        for html_f in html_files.keys():
            res = make_thumbnails_for_html_f(html_files[html_f]['images'], 
                dest_dir)
            if not res['errors']:
                html_files[html_f]['images'] = res['images_info']
            else:
                resp['result'] = '<br>'.join(res['errors'])
            
        
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
    

def url_to_ignore(url, ignored_urls):
    ''' '''
    ret_val = False
    for ig_url in ignored_urls:
        if ig_url in url:
            ret_val = True
            break
    return ret_val
    
    
def make_thumbnails_for_html_f(img_list, dest_dir):
    '''This function processes the image links found in the HTML file(s).
    It creates a "thumbs" directory, and copies the image files into there,
    if possible. It also stored a link to each thumbnail file in the images
    "thumb_name" field.
    
     html_files dict format:
        {'example2.htm':
            'path': './data/two_html_data/example2.htm'
            {'images': [
                {'orig_height': '', 
                'alt_text': u'alt text for image myfile', 
                'f_name': u'myfile.jpg', 
                'location': u'example2_files/myfile.jpg', 
                'thumb_name': ''},
                {'orig_height': '', 
                'alt_text': u'alt text for image myfile2', 
                'f_name': u'myfile2.jpg', 
                'location': u'example2_files/myfile2.jpg', 
                'thumb_name': ''}
                ],
            },
        'example2.htm': ...
        }
        
    :param img_list: a list of dicts containing images info.   
    :param dest_dir: the destination diretory for the extracted files.
    :return res: a dict containing either images info or errors.
    '''
    res = {'errors': [],
            'images_info': []}
    size = (400, 100)
    allowed_img_types = ('image/gif', 'image/png', 'image/jpeg')
    
    output_dir = os.path.join(dest_dir, 'thumbs')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    
    for i in range(0, len(img_list)):
    
        if 'http' in img_list[i]['location']:
            #This is a link to a remote resource. Download it with a request.
            url = img_list[i]['location'].strip()
#            print(url)
                    
            try:
                resp = requests.get(url)
            except Exception as exc:
                res['errors'].append(exc.__str__)
                continue
            #if resp.status_code == 200 and 
            if 'content-type' not in resp.headers.keys():
                res['errors'].append('Key not found for {}'.format(url))
                continue
            if (resp.headers['content-type'] 
                in allowed_img_types):                
                posn_last_dot = img_list[i]['f_name'].rfind('.')
                im = Image.open(StringIO(resp.content))    
                (width, height ) = im.size
                #Create thumbnails based on size
                if height > 100 or width > 400: #It's too big, make a thumbnail.
                    im.thumbnail(size)
                try:
                    if resp.headers['content-type'] == 'image/gif':
                        ext = 'gif'
                        thumb_fname = img_list[i]['f_name'][:posn_last_dot] + '_thumb.' + ext
                        thumb_fname = remove_bad_chars(thumb_fname)
                        thumb_f = os.path.join(output_dir, thumb_fname)
                        im.save(thumb_f, "GIF")
                        img_list[i]['thumb_name'] = thumb_fname
                    elif resp.headers['content-type'] == 'image/png':
                        ext = 'png'
                        thumb_fname = img_list[i]['f_name'][:posn_last_dot] + '_thumb.' + ext
                        thumb_fname = remove_bad_chars(thumb_fname)
                        thumb_f = os.path.join(output_dir, thumb_fname)
                        im.save(thumb_f, "PNG")
                        img_list[i]['thumb_name'] = thumb_fname
                    else:       
                        ext = 'jpg'
                        thumb_fname = img_list[i]['f_name'][:posn_last_dot] + '_thumb.' + ext
                        thumb_fname = remove_bad_chars(thumb_fname)
                        thumb_f = os.path.join(output_dir, thumb_fname)
                        im.save(thumb_f, "JPEG")
                        img_list[i]['thumb_name'] = thumb_fname
                except IOError as exc:
                    res['errors'].append(
                        'Cannot create thumbnail. Error: {}'.format(exc.__str__()))
                                        
        else:    
            #This is a path to a local resource
            img_full_path = os.path.join(dest_dir, img_list[i]['location'])
            try:
                #Create thumbnails based on size
                im = Image.open(img_full_path)
                (width, height) = im.size
                if height > 100 or width > 400: #It's too big, make a thumbnail.
                    posn_last_dot = img_list[i]['f_name'].rfind('.')
                    thumb_fname = img_list[i]['f_name'][:posn_last_dot] + '_thumb.jpg'
                    thumb_fname = remove_bad_chars(thumb_fname)
                    thumb_f = os.path.join(output_dir, thumb_fname)
                    im.thumbnail(size)
                    im.save(thumb_f, "JPEG")                
                    img_list[i]['thumb_name'] = thumb_fname
                else:
                    f = os.path.join(output_dir, img_list[i]['f_name'])
                    shutil.copy(img_full_path, output_dir)
                    img_list[i]['thumb_name'] = os.path.basename(img_list[i]
                                                                ['f_name'])
            except IOError as exc:
                res['errors'].append(
                    'Cannot create thumbnail for {}. Error: {}'.format(
                    img_list[i]['f_name'], exc.__str__()))
    res['images_info'] = img_list    
    return res


# Functions for parsing HTML ##################################################
def parse_file(f_name):
    '''Processes all the img tags found in one HTML file. It then stores
    the alt and src property values.
    
    :param f_name: the HTML file path & name.
    :return info: information about each image found.
    :rtype info: dict.'''
    info = []
    ignored_urls = ('emltrk.com','_ri_=')
    
    soup = BeautifulSoup(open(f_name))
    images = soup.find_all('img')
    for img in images:
        if url_to_ignore(img['src'], ignored_urls):
            continue
        img_dict = {'alt_text': '', 
                     'f_name': os.path.basename(img['src']),
                     'location': img['src'],
                     'orig_height': '',
                     'thumb_name': ''
                     }
        if img.has_attr('alt'):
            img_dict['alt_text'] = img['alt']
        info.append(img_dict)
        
    return info
