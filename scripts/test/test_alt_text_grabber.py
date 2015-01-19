#!/usr/bin/env python


'''
'''

import unittest, os, sys, shutil
import datetime as dt
sys.path.append(os.path.abspath('../..'))


from scriptpile import settings
from scripts.lib.alt_text_grabber import *


def get_test_dest_dir():
    media_root = settings.MEDIA_ROOT
    #now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    #now_sfx = ''
    #dest_dir = os.path.join(media_root, 'test_job_20150115')
    #dest_dir = os.path.join(media_root, 'test_job_20150112_so_try')
    dest_dir = os.path.join(media_root, 'test_job_20150119_pp_try')
    
    return dest_dir


class Tester(unittest.TestCase):


    def setUp(self):
        self.dest_dir = get_test_dest_dir()
       
       
    def tearDown(self):
        pass
       
   
    def test_find_all_html_files(self):
        #job_dir = './data/two_html_data'
        job_dir = self.dest_dir
        html_files = find_all_html_files(job_dir)
#        for k in html_files.keys():
#            print(k)
#            print(html_files[k])
#        self.assertEqual(html_files['example1.htm']['path'], 
#            './data/two_html_data/example1.htm')
#        self.assertEqual(html_files['example2.htm']['path'], 
#            './data/two_html_data/example2.htm')
            

#    def test_parse_file(self):
#        '''html_files dict format:
#        {'example2.htm':
#            'path': './data/two_html_data/example2.htm'
#            {'images': [
#                {'orig_height': '', 
#                'alt_text': u'alt text for image myfile', 
#                'f_name': u'myfile.jpg', 
#                'location': u'example2_files/myfile.jpg', 
#                'thumb_name': ''},
#                {'orig_height': '', 
#                'alt_text': u'alt text for image myfile2', 
#                'f_name': u'myfile2.jpg', 
#                'location': u'example2_files/myfile2.jpg', 
#                'thumb_name': ''}
#                ],
#            },
#        'example2.htm': ...
#        }
#        '''        
#        #job_dir = './data/two_html_data'
#        html_files = find_all_html_files(self.dest_dir)
#        for html_f in html_files.keys():
#            images_info = parse_file(html_files[html_f]['path'])
#            html_files[html_f]['images'] = images_info
#        self.assertIn('example1.htm', html_files.keys())
#        self.assertIn('example2.htm', html_files.keys())
#        #print(html_files)
        
        
    def test_make_thumbnails_for_html_f(self):
        #os.mkdir(self.dest_dir)
        html_files = find_all_html_files(self.dest_dir)
        for html_f in html_files.keys():
            images_info = parse_file(html_files[html_f]['path'])
            html_files[html_f]['images'] = images_info
            
#        for k, v in html_files.items():
#            print('{}:\n {}'.format(k, v))    
        
        thumbs_dir = os.path.join(self.dest_dir, 'thumbs')
        if os.path.isdir(thumbs_dir):
            shutil.rmtree(thumbs_dir)
        
        for html_f in html_files.keys():
            res = make_thumbnails_for_html_f(html_files[html_f]['images'], 
                self.dest_dir)
            if not res['errors']:
                html_files[html_f]['images'] = res['images_info']
            else:
                print(res['errors'])
        
#        for k, v in html_files.items():
#            print('{}:\n {}'.format(k, v))
    
#    def test_(self):


        
        
        
if __name__ == "__main__":
    unittest.main()
