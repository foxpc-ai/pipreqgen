import unittest
import os
import json
from reqgen.extract_imports import extract_imports, extract_imports_from_ipynb, get_versions

class TestExtractImports(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.py'
        with open(self.filename, 'w') as file:
            file.write('import os\nimport sys\nimport netmiko')

        self.emtyfile = 'empty.py'
        with open(self.emtyfile, 'w') as efile:
            efile.write('blank')

        self.fileipynb = 'test.ipynb'
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ['import numpy\n', 'import pandas as pd\n']
                }
            ]
        }
        with open(self.fileipynb, 'w') as fileipy:
            json.dump(notebook, fileipy)
        
        self.duplicatefile = 'duplicate.py'
        with open(self.duplicatefile, 'w') as dupfile:
            dupfile.write('import os\nimport netmiko\nimport netmiko\nimport flask\nimport sys\nimport sys')


    def test_extract_imports(self):
        expected_imports = ['os', 'sys', 'netmiko']
        actual_imports = extract_imports(self.filename)
        self.assertEqual(actual_imports, expected_imports)

    def test_extract_imports_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            extract_imports('nonexistent.py')


    def test_extract_imports_from_ipynb(self):
        expected_imports = ['numpy', 'pandas']
        actual_imports = extract_imports_from_ipynb('test.ipynb')
        self.assertEqual(actual_imports, expected_imports)

    def test_empty_import(self):
        expected_imports = []
        actual_imports = extract_imports(self.emtyfile)
        self.assertEqual(actual_imports, expected_imports)


    def test_extract_imports_from_ipynb_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            extract_imports_from_ipynb('nonexistent.ipynb')

    def test_get_versions(self):
        modules = ['os', 'sys', 'non_existent_module']
        expected_versions = {
            'os': 'os not found',
            'sys': 'sys not found',
            'non_existent_module': 'non_existent_module not found'
        }
        actual_versions = get_versions(modules,append=True)
        self.assertEqual(actual_versions, expected_versions)

    # def test_get_versions_empty_list(self):
    #     with self.assertRaises(ValueError):
    #         get_versions([])
        
    def test_duplicate_imports(self):
        expected_imports = ['os','netmiko','flask','sys']
        actual_imports = extract_imports(self.duplicatefile)
        self.assertEqual(actual_imports, expected_imports)

    def tearDown(self):
        try:
            os.remove(self.filename)
            os.remove(self.emtyfile)
            os.remove(self.duplicatefile)
            os.remove(self.fileipynb)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    unittest.main()
