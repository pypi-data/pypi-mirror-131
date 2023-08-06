# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from datetime import datetime


class PimMemoTestCase(ModuleTestCase):
    'Test memo module'
    module = 'pim_memos'

    @with_transaction()
    def test_pimmemo_create_item(self):
        """ create memo
        """
        pool = Pool()
        PimMemo = pool.get('pim_memos.note')
        
        m1 = PimMemo(memo = 'text 1')
        m1.save()
        
        m_lst = PimMemo.search([])
        self.assertEqual(len(m_lst), 1)
        self.assertEqual(m_lst[0].memo, 'text 1')
        self.assertEqual(m_lst[0].name, 'text 1')
        self.assertEqual(m_lst[0].title, None)
        self.assertEqual(m_lst[0].memoshort, 'text 1')
        
        m2_lst = PimMemo.search([('memo', '=', 'text 1')])
        self.assertEqual(len(m2_lst), 1)
        m2_lst = PimMemo.search([('memo', 'ilike', '%text%')])
        self.assertEqual(len(m2_lst), 1)

        m2_lst = PimMemo.search([('name', '=', 'text 1')])
        self.assertEqual(len(m2_lst), 1)
        m2_lst = PimMemo.search([('name', 'ilike', '%text%')])
        self.assertEqual(len(m2_lst), 1)

        m2_lst = PimMemo.search([('memoshort', '=', 'text 1')])
        self.assertEqual(len(m2_lst), 1)
        m2_lst = PimMemo.search([('memoshort', 'ilike', '%text%')])
        self.assertEqual(len(m2_lst), 1)

    @with_transaction()
    def test_pimmemo_create_item_tree(self):
        """ create memo, add sub-items
        """
        pool = Pool()
        PimMemo = pool.get('pim_memos.note')
        
        m1 = PimMemo(memo = 'text 1')
        m1.save()
        m_lst = PimMemo.search([])
        self.assertEqual(len(m_lst), 1)

        m2 = PimMemo(memo = 'text 2', parent = m1)
        m2.save()
        m_lst = PimMemo.search([], order=[('memo', 'ASC')])
        self.assertEqual(len(m_lst), 2)
        self.assertEqual(m_lst[0].memo, 'text 1')
        self.assertEqual(m_lst[0].parent, None)
        self.assertEqual(m_lst[0].childs, (m2,))
        
        self.assertEqual(m_lst[1].memo, 'text 2')
        self.assertEqual(m_lst[1].parent, m1)
        self.assertEqual(m_lst[1].childs, ())
        
        # delete root item, should fail
        self.assertRaisesRegex(UserError, 
            "The note 'text 1' has subnotes and therefore can not be deleted.",
            PimMemo.delete,
            [m1])

    @with_transaction()
    def test_pimmemo_create_item_check_sequence(self):
        """ create memo2, check sequence
        """
        pool = Pool()
        PimMemo = pool.get('pim_memos.note')
        
        m1 = PimMemo(memo = 'text 1', sequence=1)
        m1.save()
        m2 = PimMemo(memo = 'text 2', sequence=2)
        m2.save()

        # default-order is 'by sequence'
        m_lst = PimMemo.search([])
        self.assertEqual(len(m_lst), 2)
        self.assertEqual(m_lst[0].memo, 'text 1')
        self.assertEqual(m_lst[1].memo, 'text 2')
        
        m1.sequence = 3
        m1.save()

        m_lst = PimMemo.search([])
        self.assertEqual(len(m_lst), 2)
        self.assertEqual(m_lst[0].memo, 'text 2')
        self.assertEqual(m_lst[1].memo, 'text 1')

        # order by memoshort
        m_lst = PimMemo.search([], order=[('memoshort', 'ASC')])
        self.assertEqual(len(m_lst), 2)
        self.assertEqual(m_lst[0].memo, 'text 1')
        self.assertEqual(m_lst[1].memo, 'text 2')

        m_lst = PimMemo.search([], order=[('memoshort', 'DESC')])
        self.assertEqual(len(m_lst), 2)
        self.assertEqual(m_lst[0].memo, 'text 2')
        self.assertEqual(m_lst[1].memo, 'text 1')

        # order by name
        m_lst = PimMemo.search([], order=[('name', 'ASC')])
        self.assertEqual(len(m_lst), 2)
        self.assertEqual(m_lst[0].memo, 'text 1')
        self.assertEqual(m_lst[1].memo, 'text 2')

        m_lst = PimMemo.search([], order=[('name', 'DESC')])
        self.assertEqual(len(m_lst), 2)
        self.assertEqual(m_lst[0].memo, 'text 2')
        self.assertEqual(m_lst[1].memo, 'text 1')

    @with_transaction()
    def test_pimmemo_create_item_tree_with_recursion(self):
        """ create memo, add sub-items, add recursion
        """
        pool = Pool()
        PimMemo = pool.get('pim_memos.note')
        
        m1 = PimMemo(memo = 'text 1')
        m1.save()
        m_lst = PimMemo.search([])
        self.assertEqual(len(m_lst), 1)

        m2 = PimMemo(memo = 'text 2', parent = m1)
        m2.save()
        m_lst = PimMemo.search([], order=[('memo', 'ASC')])
        self.assertEqual(len(m_lst), 2)

        # recursion, should fail
        m2.childs = [m1]
        self.assertRaisesRegex(UserError,
            'Record "text 1" with parent "text 2" was configured as ancestor of itself.',
            m2.save)

    @with_transaction()
    def test_pimmemo_create_item_with_category(self):
        """ create memo and category
        """
        pool = Pool()
        PimMemo = pool.get('pim_memos.note')
        PimCategory = pool.get('pim_memos.category')
        
        m1 = PimMemo(
                memo = 'text 1', 
                category = PimCategory(
                        name = 'cat 1'
                    )
            )
        m1.save()
        
        m_lst = PimMemo.search([])
        self.assertEqual(len(m_lst), 1)
        self.assertEqual(m_lst[0].memo, 'text 1')
        self.assertEqual(m_lst[0].category.name, 'cat 1')
        
        c_lst = PimCategory.search([])
        self.assertEqual(len(c_lst), 1)

    @with_transaction()
    def test_pimmemo_create_category(self):
        """ create a category for memos
        """
        pool = Pool()
        PimCategory = pool.get('pim_memos.category')
        
        c1 = PimCategory(
                name = 'cat 1'
            )
        c1.save()
        
        c_lst = PimCategory.search([])
        self.assertEqual(len(c_lst), 1)
        
        c2_lst = PimCategory.search([('name', '=', 'cat 1')])
        self.assertEqual(len(c_lst), 1)
        c2_lst = PimCategory.search([('name', 'ilike', '%cat%')])
        self.assertEqual(len(c_lst), 1)

    @with_transaction()
    def test_pimmemo_create_category_tree(self):
        """ create a category for memos
        """
        pool = Pool()
        PimCategory = pool.get('pim_memos.category')
        
        c1 = PimCategory(
                name = 'cat 1',
                childs = [
                    PimCategory(name='cat 2'),
                    ]
            )
        c1.save()
        
        c_lst = PimCategory.search([], order=[('name', 'ASC')])
        self.assertEqual(len(c_lst), 2)
        self.assertEqual(c_lst[0].name, 'cat 1')
        self.assertEqual(c_lst[0].parent, None)
        self.assertEqual(len(c_lst[0].childs), 1)
        self.assertEqual(c_lst[0].childs[0].name, 'cat 2')
        
        self.assertEqual(c_lst[1].name, 'cat 2')
        self.assertEqual(c_lst[1].parent.name, 'cat 1')
        self.assertEqual(len(c_lst[1].childs), 0)
        
        # delete root-category, should fail
        self.assertRaisesRegex(UserError,
            "The category 'cat 1' has subcategories and therefore can not be deleted.",
            PimCategory.delete,
            [c1])

# end PimMemoTestCase
