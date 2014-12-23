from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
#from django.http import HttpResponse

from scripts.lib.alt_text_grabber import handle_uploaded_f


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
            resp = handle_uploaded_f(settings.MEDIA_ROOT, request.FILES['fileToUpload'])
        else:
            pass
        return render_to_response('alt_text_confirm.html', resp)
    


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
    
    
