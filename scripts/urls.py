from django.conf.urls import patterns, url

from scripts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^alt_text_grabber$', views.alt_text_grabber, name='alt_text_grabber'),
    url(r'^test_form$', views.test_form, name='test_form'),
    url(r'^file_uploader$', views.file_uploader, name='file_uploader')
    #url(r'^scriptpile/scripts$', views.index, name='index')
)