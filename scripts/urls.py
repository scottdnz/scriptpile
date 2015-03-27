from django.conf.urls import patterns, url

from scripts import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^alt_text_grabber$', views.alt_text_grabber, name='alt_text_grabber'),
    url(r'^link_resolver_upload$', views.link_resolver_upload, name='link_resolver_upload'),
    url(r'^link_resolver_confirm$', views.link_resolver_confirm, name='link_resolver_confirm'),
    url(r'^link_resolver$', views.link_resolver, name='link_resolver'),
    url(r'^test_form$', views.test_form, name='test_form'),
    url(r'^file_uploader$', views.file_uploader, name='file_uploader'),
    url(r'^store_encrypted$', views.store_encrypted, name='store_encrypted'),
    url(r'^gsearch$', views.gsearch, name='gsearch'),
    url(r'^gsearch_requester$', views.gsearch_requester, name='gsearch_requester')
    #url(r'^scriptpile/scripts$', views.index, name='index')
)
