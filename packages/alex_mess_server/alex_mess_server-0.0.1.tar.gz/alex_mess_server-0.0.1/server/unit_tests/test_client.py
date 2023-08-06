"""Unit-тесты клиента"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS
from client import Client


class TestClassClient(unittest.TestCase):
    cl = Client(DEFAULT_IP_ADDRESS, DEFAULT_PORT, 'Guest')

    def test_def_presense(self):
        """Тест коректного запроса"""
        class_method = self.cl.create_presence()
        class_method[TIME] = 1.1
        self.assertEqual(class_method, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_answer(self):
        """Тест корректного разбора ответа 200"""
        self.assertEqual(self.cl.process_for_answer({RESPONSE: 200}), '200 : OK')

    def test_400_answer(self):
        """Тест корректного разбора 400"""
        self.assertEqual(self.cl.process_for_answer({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, self.cl.process_for_answer, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
