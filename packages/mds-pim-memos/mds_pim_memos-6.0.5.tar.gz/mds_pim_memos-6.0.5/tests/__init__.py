# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.pim_memos.tests.test_memos import PimMemoTestCase

__all__ = ['suite']



class PimMemoModuleTestCase(\
            PimMemoTestCase):
    'Test memo module'
    module = 'pim_memos'

#end PimMemoModuleTestCase


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PimMemoModuleTestCase))
    return suite
