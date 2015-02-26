'''
Created on Jan 19, 2015

@author: jcabezas
'''

import unittest

import test_style
import test_utils

if __name__ == '__main__':
    for module in [ test_style, test_utils ]:
        suite = unittest.TestLoader().loadTestsFromModule(module)
        unittest.TextTestRunner(verbosity=2).run(suite)