'''
Created on Jan 19, 2015

@author: jcabezas
'''
import unittest

import figplotter.utils as orig
import figplotter.plot.defaults as orig_defaults

class Test(unittest.TestCase):
    def test_parameter_update(self):
        # Update disjoint elements
        p1 = orig.Parameter({'A': 1})
        p2 = orig.Parameter({'B': 2})
        p1.update(p2)
        expected = orig.Parameter({'A': 1, 'B': 2})
        self.assertEqual(p1, expected, 'failed at update disjoint elements')

        # Update overlapping elements
        p1 = orig.Parameter({'A': 1, 'B': 2})
        p2 = orig.Parameter({'B': 3, 'C': 4})
        p1.update(p2)
        expected = orig.Parameter({'A': 1, 'B': 3, 'C': 4})
        self.assertEqual(p1, expected, 'failed at update overlapping elements')

        # Update same default
        p1 = orig.Parameter({'*': 1, 'A': 2})
        p2 = orig.Parameter({'*': 1, 'B': 3})
        p1.update(p2)
        expected = orig.Parameter({'*': 1, 'A': 2, 'B': 3})
        self.assertEqual(p1, expected, 'failed at update same default')
        
        # Update different default
        p1 = orig.Parameter({'*': 1, 'A': 2})
        p2 = orig.Parameter({'*': 2, 'B': 4})
        try:
            p1.update(p2)
            self.assertTrue(False, 'failed at update different default')
        except:
            self.assertTrue(True)
            
        # Update same base values
        p1 = orig_defaults.BaseParameter({'_': 1, 'A': 2})
        p2 = orig_defaults.BaseParameter({'_': 1, 'B': 3})
        try:
            p1.update(p2)
            self.assertTrue(False, 'failed at update same base values')
        except:
            self.assertTrue(True)
            
        # Update different base values
        p1 = orig_defaults.BaseParameter({'_': 1, 'A': 2})
        p2 = orig_defaults.BaseParameter({'_': 2, 'B': 4})
        try:
            p1.update(p2)
            self.assertTrue(False, 'failed at update different base values')
        except:
            self.assertTrue(True)

    def test_parameter_set_series(self):
        # Single value broadcasting
        p = orig.Parameter(2)
        p.set_series(['A', 'B', 'C'])
        expected = orig.Parameter({ 'A': 2,
                                    'B': 2,
                                    'C': 2 })
        self.assertEqual(p, expected, 'failed at single value broadcasting')

        # Values in iterable
        p = orig.Parameter([1, 2, 3])
        p.set_series(['A', 'B', 'C'])
        expected = orig.Parameter({ 'A': 1,
                                    'B': 2,
                                    'C': 3 })
        self.assertEqual(p, expected, 'failed at values in iterable')
        
        # Values in mapping
        p = orig.Parameter({'A': 1, 'B': 2, 'C': 3})
        p.set_series(['A', 'B', 'C'])
        expected = orig.Parameter({ 'A': 1,
                                    'B': 2,
                                    'C': 3 })
        self.assertEqual(p, expected, 'failed at values in mapping')
        
        # Add new series with no default value
        p = orig.Parameter({'A': 1, 'B': 2, 'C': 3})
        p.set_series(['A', 'B', 'C', 'D'])
        expected = orig.Parameter({ 'A': 1,
                                    'B': 2,
                                    'C': 3 })
        self.assertEqual(p, expected, 'failed at add new series with no default values')

        # Add new series with default value
        p = orig.Parameter({'A': 1, 'B': 2, 'C': 3, '*': 0})
        p.set_series(['A', 'B', 'C', 'D', 'E'])
        expected = orig.Parameter({ '*': 0,
                                    'A': 1,
                                    'B': 2,
                                    'C': 3,
                                    'D': 0,
                                    'E': 0 })
        self.assertEqual(p, expected, 'failed at add new series with default value')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()