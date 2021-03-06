from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse
from apiclient.discovery import build

import logging, json, csv

from scripts.lib.alt_text_grabber import handle_uploaded_f
from scripts.lib.link_resolver import (handle_link_f, read_csv_file, 
    try_each_link)
from scripts.lib.basic_db_access import (connect_to_db, insert_secret_vals, 
    encrypt_val, decrypt_val)
from scripts.lib.google_search import (get_api_keys, get_req_result_set, 
search_google)
from scripts.lib.email_hasher import handle_uploaded_email_f


#def index(request):
#test_vals = {'val1': 'value1'}
#    return render(request, 'index.html', test_vals)
#    return HttpResponse('Hello, world. You're at the scripts index.')

def index(request):
    return render(request, 'index.html')


def alt_text_grabber(request):
    if request.method == 'GET':
        return render(request, 'alt_text_grabber.html')
    elif request.method == 'POST':
        if request.FILES.has_key('fileToUpload'):
            resp = handle_uploaded_f(settings.MEDIA_ROOT, 
                request.FILES['fileToUpload'])
            resp['host_ref'] = settings.HOST_REF
        else:
            pass
        return render_to_response('alt_text_confirm.html', resp)
        
        
def link_resolver_upload(request):
    if request.method == 'GET':
        return render(request, 'link_resolver_upload.html')
    elif request.method == 'POST':
        resp = {}
        if not request.POST.has_key('format'):
            resp['errors'] = ['Format key missing.',]
        elif not request.FILES.has_key('fileToUpload'):
            resp['errors'] = ['Please choose a file',]
        else:
            resp = handle_link_f(settings.MEDIA_ROOT, 
                    request.FILES['fileToUpload'], request.POST['format'])
        return render(request, 'link_resolver_confirm.html', resp)
        
        
def link_resolver_confirm(request):
    if request.method == 'GET':
        return render(request, 'link_resolver_confirm.html')
    elif request.method == 'POST':
        resp = {'cols_to_check': [], 'errors': [], 'url_prefix': '',
            'path_to_f': request.POST['path_to_f'], 
            'separator': str(request.POST['separator']),
            'links_rows': {}
             }
        for i in range(6):
            col_to_check = 'col{}ForURL'.format(i)
            if request.POST.has_key(col_to_check) and request.POST[
                col_to_check] != 'none':
                resp['cols_to_check'].append(request.POST[col_to_check])
                
        if request.POST['urlPrefixY'] == 'y' and (
            not request.POST.has_key('urlPrefix') or 
            len(request.POST['urlPrefix']) == 0):
            resp['errors'].append(
            'Please choose a URL prefix. Click Go Back to start again.')
        
        elif request.POST['urlPrefixY'] == 'y' and (
            len(request.POST['urlPrefix']) > 0):
            resp['url_prefix'] = request.POST['urlPrefix']
        
        resp['host_ref'] = settings.HOST_REF    
        resp['links_rows'] = read_csv_file(resp['path_to_f'], resp['separator'], 
            resp['cols_to_check'], resp['url_prefix'])
        

        res = try_each_link(resp['links_rows'], settings.MEDIA_ROOT)
        if len(res['errors']) > 0:
            resp['errors'] += res['errors']
        resp['links_rows'] = res['links_rows']
        resp['dest_dir'] = res['dest_dir']
            
        if len(resp['errors']) > 0:
            return render(request, 'link_resolver_confirm.html', resp)
        else:    
            return render(request, 'link_resolver.html', resp)
        
        
def gsearch(request):
    if request.method == 'GET':
        return render(request, 'gsearch_form.html')
        
        
def gsearch_requester(request):
    if request.method == 'POST':
        data = {"results": []}
        
        #print(request.META.get('CONTENT_TYPE'))
        #print(request.POST)
        rec_json_data=json.loads(request.body)
        search_terms = rec_json_data['search_terms']
        start_val = int(rec_json_data['start_val'])
        #print(rec_json_data['search_terms'])
        
        res = connect_to_db(username=settings.DATABASES['default']['USER'], 
        password=settings.DATABASES['default']['PASSWORD'], 
        database=settings.DATABASES['default']['NAME'])
        # Get Google API keys from the DB & unencrypt them
        project_lbl = 'custom search engine1'
        api_lbl = 'testSearch1 Project - api key'
        api_keys = get_api_keys(res['db_conn'], project_lbl, api_lbl)
        #print(api_keys)
        api_keys['project_key'] = decrypt_val(api_keys['project_key'], 
           settings.ENCR_KEY, settings.ENCR_IV)
        api_keys['api_key'] = decrypt_val(api_keys['api_key'],
           settings.ENCR_KEY, settings.ENCR_IV)
    
        info = {'search_text': search_terms,
        'num_requests': 10,
        'search_engine_id': api_keys['project_key'],
        'api_key': api_keys['api_key']
        }
        
        results = []
        service = build('customsearch', 'v1', developerKey=info['api_key'])
        collection = service.cse()
        # This is the offset from the beginning to start getting the results from
        #start_val = 1 + (i * 10)
        data["results"].append(get_req_result_set(collection, start_val, info))
        
        
        
        return HttpResponse(json.dumps(data), content_type='application/json')
        
        
        
def link_resolver(request):
    if request.method == 'GET':
        return render(request, 'link_resolver.html')
    elif request.method == 'POST':
        pass
    

def test_form(request):
    if request.method == 'GET':
        return render(request, 'test_form.html')
    elif request.method == 'POST':
        resp = {'firstName': '',
                'category': '',
                'longText': ''}
        if request.POST.has_key('firstName'):
            resp['firstName'] = request.POST.get('firstName')
        if request.POST.has_key('firstName'):
            resp['category'] = request.POST.get('category')
        if request.POST.has_key('longText'):
            resp['longText'] = request.POST.get('longText')
        return render_to_response('test_form_confirm.html', resp)
    

def file_uploader(request):
    if request.method == 'GET':
        return render(request, 'file_uploader.html')
    elif request.method == 'POST':
        resp = {'result': 'good'}
        if request.FILES.has_key('fileToUpload'):
            resp['f_name'] = ''
            try:
                handle_uploaded_f(settings.MEDIA_ROOT, request.FILES['fileToUpload'])
            except Exception as exc:
                resp['result'] = 'bad, ' + exc.__str__()    
        return render_to_response('file_uploader_confirm.html', resp)
        
        
def store_encrypted(request):
    resp = {'result': 'good'}
    logger = logging.getLogger(__name__)
    
    if request.method == 'GET':
        return render(request, 'store_encrypted.html')
    elif request.method == 'POST':
        resp = {'result': 'good'}
        #Check all keys are present
        compulsory_keys = ('label', 'plainValue')
        for ck in compulsory_keys:
            if not request.POST.has_key(ck):
                resp['result'] = 'bad'
        if not resp['result'] == 'good':
            return render_to_response('store_encrypted.html', resp)
        # Get form field vals    
        label = request.POST.get('label')
        plain_val = request.POST.get('plainValue')
        
        
        #res = connect_to_db(username='scriptuser', password='password', 
#            database='scriptpile')
            
        res = connect_to_db(username=settings.DATABASES['default']['USER'], 
        password=settings.DATABASES['default']['PASSWORD'], 
            database=settings.DATABASES['default']['NAME'])            
            
        if len(res['error']) > 0:
            resp['result'] = res['error']
        else:
            insert_secret_vals(res['db_conn'], label, plain_val, 
            settings.ENCR_KEY, settings.ENCR_IV, logger)       
            
            resp['result'] = 'Success'
        return render_to_response('store_encrypted.html', resp)          


def email_hasher(request):
    if request.method == 'GET':
        return render(request, 'email_hasher.html')
    elif request.method == 'POST':
        if request.FILES.has_key('fileToUpload'):
            resp = handle_uploaded_email_f(settings.MEDIA_ROOT, 
                request.FILES['fileToUpload'])
            resp['host_ref'] = settings.HOST_REF 
        else:
            pass
        return render_to_response('email_hasher_confirm.html', resp)


def email_hasher_return_encrypted_file(request):
    # Create the HttpResponse object with the appropriate CSV header.
    f_name = settings.MEDIA_ROOT + '/' +  request.GET['fldr'] + '/encrypted_emails.csv'
    f = open(f_name, 'rb')
    enc_emails = f.readlines()
    f.close()
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerows([[enc_email.strip()] for enc_email in enc_emails])
    
    #print('filename="{}/encrypted_emails.csv"'.format(fldr))
    response['Content-Disposition'] = 'attachment; filename="encrypted_emails.csv"'
    
    return response