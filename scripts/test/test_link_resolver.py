#!/usr/bin/env python


'''
'''

import unittest, os, sys, shutil
import datetime as dt
sys.path.append(os.path.abspath('../..'))


from scriptpile import settings
from scripts.lib.link_resolver import *


def get_test_dest_dir():
    media_root = settings.MEDIA_ROOT
    dest_dir = os.path.join(media_root, 'test_job_20150119_lt')
    
    return dest_dir


class Tester(unittest.TestCase):


    def setUp(self):
        self.dest_dir = get_test_dest_dir()
       
       
    def tearDown(self):
        pass
       
   
    #def test_get_col_headings(self):
    #    path_to_f = os.path.join(self.dest_dir, 'test_f_an_v2.txt')
    #    fieldnames = get_col_headi ngs(path_to_f, separator='|')
    #    self.assertEqual(len(fieldnames), 35)
        
    
    #def test_read_csv_file(self):
    #    path_to_f = os.path.join(self.dest_dir, 'test_f_an_v2.txt')
    #    cols_to_check = ['PXT1_GROUP', 'PXT2_GROUP']
    #    prefix = 'https://flybuys-permissionnzltd.netdna-ssl.com/partners/'
    #    links_rows = read_csv_file(path_to_f, '|', cols_to_check, 
    #        prefix)
        
    #    for k, v in links_rows.items():
    #        print('{}: ' .format(k))
            #for url_dic in v:
            #    for url_k, url_v in url_dic.items():
            #        print('\t{}: {}\n******'.format(url_k, url_v))
            
            #for url_k, url_v in v.items():
            #    print('\t{}: {}\n******'.format(url_k, url_v))
     #       print(len(v.keys()))
            
       
    def test_try_each_link(self):
        path_to_f = os.path.join(self.dest_dir, 'test_f_an_v2.txt')
        cols_to_check = ['PXT1_GROUP', 'PXT2_GROUP']
        prefix = ''
        links_rows = read_csv_file(path_to_f, '|', cols_to_check, prefix)
        
        res = try_each_link(links_rows)
        links_rows = res['links_rows']
        for k, v in links_rows.items():
            print('****\n{}: ' .format(k))  
            for url_k, url_v in v.items():
                print('\t{}: {}\n******'.format(url_k, url_v))

    #    def test_(self):
  
        
if __name__ == "__main__":
    unittest.main()
