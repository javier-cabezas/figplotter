'''
Created on Jan 19, 2015

@author: jcabezas
'''
import unittest

import figplotter.plot.style as orig
from figplotter.utils import Parameter

class TestBase(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_build_dict(self):
        style_dict = {'*': { 'first::second': 0 }}
        
        expected = {'first_params': { 'second' : Parameter({ '*': 0 }) }}
        d = orig.build_dict(('*', style_dict['*']))
        self.assertEqual(d, expected, 'failed at wrong registered params')
        
        d = orig.build_dict(('*', style_dict['*']))
        self.assertEqual(d, expected, 'failed at valid arguments')


    def test_generate_params1(self):
        style_dict = {'*': { 'first::second': 0 },
                      'A': { 'first::second': 1 }}

        expected = {'first_params': { 'second' : Parameter({ 'A': 1 }) }}
        d = orig.generate_params(style_dict, [['A']])
        self.assertEqual(d, expected, 'failed at wrong registered params')

        expected = {'first_params': { 'second' : Parameter({ 'A': 1, 'B': 0 }) }}
        d = orig.generate_params(style_dict, [['A', 'B']])
        self.assertEqual(d, expected, 'failed at valid arguments')


    def test_generate_params2(self):
        style_dict = {'*': { 'first::second': 0 },
                      'A': { 'first2::second2': 1 }}

        expected = {'first_params':  { 'second' : Parameter({ 'A': 0 }) },
                    'first2_params': { 'second2': Parameter({ 'A': 1 }) }}
        d = orig.generate_params(style_dict, [['A']])
        self.assertEqual(d, expected, 'failed at wrong registered params')

        expected = {'first_params':  { 'second' : Parameter({ 'A': 0, 'B': 0 }) },
                    'first2_params': { 'second2': Parameter({ 'A': 1 }) }}
        d = orig.generate_params(style_dict, [['A', 'B']])
        self.assertEqual(d, expected, 'failed at valid arguments')


    def test_generate_params3(self):
        style_dict = {'*::*': { 'first::second': 0 },
                      'A::1': { 'first::second': 1 }}

        expected = {'first_params': { 'second' : Parameter({ 'A::1': 1 }) }}
        d = orig.generate_params(style_dict, [['A'], ['1']])
        self.assertEqual(d, expected, 'failed at wrong registered params')

        expected = {'first_params': { 'second' : Parameter({ 'A::1': 1, 'A::2': 0,
                                                             'B::1': 0, 'B::2': 0 }) }}
        d = orig.generate_params(style_dict, [['A', 'B'], ['1', '2']])
        self.assertEqual(d, expected, 'failed at valid arguments')


    def test_generate_params4(self):
        style_dict = {'*::*': { 'first::second': 0 },
                      'A::1': { 'first2::second2': 1 }}

        expected = {'first_params':  { 'second' : Parameter({ 'A::1': 0 }) },
                    'first2_params': { 'second2': Parameter({ 'A::1': 1 }) }}
        d = orig.generate_params(style_dict, [['A'], ['1']])
        self.assertEqual(d, expected, 'failed at wrong registered params')

        expected = {'first_params':  { 'second' : Parameter({ 'A::1': 0, 'A::2': 0,
                                                              'B::1': 0, 'B::2': 0 }) },
                    'first2_params': { 'second2': Parameter({ 'A::1': 1 }) }}
        d = orig.generate_params(style_dict, [['A', 'B'], ['1', '2']])
        self.assertEqual(d, expected, 'failed at valid arguments')

Tests = [ TestBase ]

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()