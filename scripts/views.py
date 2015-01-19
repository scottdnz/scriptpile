from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
#from django.http import HttpResponse

from scripts.lib.alt_text_grabber import handle_uploaded_f
from scripts.lib.link_resolver import (handle_link_f, read_csv_file, 
    try_each_link)


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
            
        resp['links_rows'] = read_csv_file(resp['path_to_f'], resp['separator'], 
            resp['cols_to_check'], resp['url_prefix'])
        

        res = try_each_link(resp['links_rows'])
        if len(res['errors']) > 0:
            resp['errors'] += res['errors']
        resp['links_rows'] = res['links_rows']
            
        if len(resp['errors']) > 0:
            return render(request, 'link_resolver_confirm.html', resp)
        else:    
            return render(request, 'link_resolver.html', resp)
        
                
        
        
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
