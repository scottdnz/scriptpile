import requests, os, zipfile
import datetime as dt


def handle_uploaded_f(media_root, f):
    ''' '''
    resp = {}
    resp['result'] = ''
    full_path = media_root + '/' + f.name
    try:
        with open(full_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        
        res = unzip_zip_arch(media_root, f.name)
                
    except Exception as exc:
        resp['result'] = 'There was a problem: ' + exc.__str__() 
    return resp


def unzip_zip_arch(media_dir, zf_name):
    '''Unzips a zipped file container (.zip format) and saves the extracted 
    files inside to a directory named like 'job_yyyymmdd_hhmmss'. '''
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    upload_z_file = os.path.join(media_dir, zf_name)
    dest_dir = os.path.join(media_dir,  'job_' + now_sfx)
    os.mkdir(dest_dir)    
    with zipfile.ZipFile(upload_z_file, 'r') as z:
        z.extractall(dest_dir)
    res = 'Zip file "{}" unzipped to {}'.format(upload_z_file, dest_dir)
    #os.remove(upload_z_file)
    return res