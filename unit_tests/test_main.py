from unittest import TestCase
import unittest
from unittest.mock import patch
from main import check_document_existance, \
    get_doc_owner_name, \
    get_all_doc_owners_names, \
    remove_doc_from_shelf, \
    add_new_shelf, \
    append_doc_to_shelf, \
    get_doc_shelf, \
    move_doc_to_shelf, \
    show_document_info, \
    add_new_doc,\
    delete_doc, \
    documents, directories


def mock_sequence_input(*args, **kwargs):
    if 'Введите номер документа - ' == args[0]:
        return '11-2'
    elif 'Введите номер полки - ' == args[0]:
        return '1'
    elif 'Введите номер полки для перемещения - ' == args[0]:
        return '3'
    elif 'Введите тип документа - ' == args[0]:
        return 'insurance'
    elif 'Введите имя владельца документа- ' == args[0]:
        return 'test'
    elif 'Введите номер полки для хранения - ' == args[0]:
        return '3'


class TestLibFuncs(TestCase):

    def test_check_document_existance(self):
        result = check_document_existance('2207 876234')
        self.assertEqual(result, True)
        result = check_document_existance('2207')
        self.assertEqual(result, False)

    @patch('builtins.input', return_value='2207 876234')
    def test_get_doc_owner_name(self, foo):
        self.assertEqual(get_doc_owner_name(), 'Василий Гупкин')

    def test_get_all_doc_owners_names(self):
        result = get_all_doc_owners_names()
        self.assertEqual(type(result), set, 'Result expected to be set')

    def test_remove_doc_from_shelf(self):
        remove_doc_from_shelf('2207 876234')
        for dirs in directories.values():
            self.assertNotIn('2207 876234', dirs)

    def test_add_new_shelf(self):
        shelf, status = add_new_shelf('4')
        self.assertEqual((shelf, status), ('4', True))

    def test_append_doc_to_shelf(self):
        append_doc_to_shelf('123', '4')
        self.assertIn('4', directories)
        self.assertIn('123', directories['4'])

    @patch('builtins.input', return_value='10006')
    def test_delete_doc(self, foo):
        self.assertEqual(delete_doc(), ('10006', True))

    @patch('builtins.input', return_value='11-2')
    def test_get_doc_shelf(self, foo):
        self.assertEqual(get_doc_shelf(), '1')

    @patch('builtins.input', new=mock_sequence_input)
    @patch('builtins.print')
    def test_move_doc_to_shelf(self, foo):
        move_doc_to_shelf()
        self.assertEqual('Документ номер "11-2" был перемещен на полку номер "3"', foo.call_args[0][0])

    @patch('builtins.print')
    def test_show_document_info(self, foo):
        show_document_info(documents[1])
        self.assertEqual('invoice "11-2" "Геннадий Покемонов"', foo.call_args[0][0])

    @patch('builtins.input', new=mock_sequence_input)
    def test_add_new_doc(self):
        self.assertEqual(add_new_doc(), '3')


if __name__ == '__main__':
    unittest.main()