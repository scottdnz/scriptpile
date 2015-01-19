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
       
   
    def test_get_col_headings(self):
        path_to_f = os.path.join(self.dest_dir, 'test_f_an_v2.txt')
        fieldnames = get_col_headings(path_to_f, separator='|')
        self.assertEqual(len(fieldnames), 35)
        
    
    


    #    def test_(self):
  
        
if __name__ == "__main__":
    unittest.main()
