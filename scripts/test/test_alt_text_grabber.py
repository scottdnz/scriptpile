#!/usr/bin/env python


'''
'''

import unittest, os, sys
sys.path.append(os.path.abspath('../..'))


from scriptpile import settings
from scripts.lib.alt_text_grabber import *


class Tester(unittest.TestCase):


    def setUp(self):
        pass
       
       
    def tearDown(self):
        pass
       
   
    def test_find_all_html_files(self):
        dest_dir = './data/two_html_data'
        html_files = find_all_html_files(dest_dir)
        
#        for k in html_files.keys():
#            print(k)
#            print(html_files[k])
        self.assertEqual(html_files['example1.htm']['path'], 
            './data/two_html_data/example1.htm')
        self.assertEqual(html_files['example2.htm']['path'], 
            './data/two_html_data/example2.htm')
            
        
        
if __name__ == "__main__":
    unittest.main()
