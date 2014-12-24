import requests, os, zipfile
from bs4 import BeautifulSoup
import datetime as dt


def handle_uploaded_f(media_root, f):
    ''' '''
    resp = {'result': '',
            'html_files': {}}
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    full_path = media_root + '/' + f.name
    dest_dir = os.path.join(media_root,  'job_' + now_sfx)
    #try:
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    res = unzip_zip_arch(media_root, f.name, dest_dir)
    
    html_files = find_all_html_files(dest_dir)
    
    for html_f in html_files.keys():
        images_info = parse_file(html_files[html_f]['path'])
        html_files[html_f]['images'] = images_info
    
    resp['html_files'] = html_files
    relative_media_dir = media_root.replace('/var/www/html/py/django_projects/scriptpile','')
    resp['dest_dir'] = os.path.join(relative_media_dir,  'job_' + now_sfx)   
       
 #   except Exception as exc:
 #       resp['result'] = 'There was a problem: ' + exc.__str__() 
    return resp


def unzip_zip_arch(media_dir, zf_name, dest_dir):
    '''Unzips a zipped file container (.zip format) and saves the extracted 
    files inside to a directory named like 'job_yyyymmdd_hhmmss'. '''
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    upload_z_file = os.path.join(media_dir, zf_name)
    
    os.mkdir(dest_dir)    
    with zipfile.ZipFile(upload_z_file, 'r') as z:
        z.extractall(dest_dir)
    res = 'Zip file "{}" unzipped to {}'.format(upload_z_file, dest_dir)
    os.remove(upload_z_file)
    return res


def find_all_html_files(job_dir):
    '''Examines files extracted in a job_x directory. '''
    html_files = {}
    for f in os.listdir(job_dir):
        if '.htm' in f:
            html_files[f] = {'path': os.path.join(job_dir, f),
                             'images': []}
    return html_files


# Functions for parsing HTML #################################################################
def parse_file(f_name):
    info = []
    soup = BeautifulSoup(open(f_name))
    images = soup.find_all('img')
    for img in images:
        info.append({'alt_text': img['alt'], 
                     'f_name': os.path.basename(img['src']),
                     'location': img['src']
                     })
    return info