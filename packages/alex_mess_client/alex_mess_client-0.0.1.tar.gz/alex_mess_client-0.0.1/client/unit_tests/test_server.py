"""Unit-тесты сервера"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT
from server import Server


class TestClassServer(unittest.TestCase):
    err_dict = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok_dict = {RESPONSE: 200}
    srv = Server(DEFAULT_IP_ADDRESS, DEFAULT_PORT)

    def test_no_action(self):
        """Ошибка - нет действия"""
        self.assertEqual(self.srv.process_for_answer({TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        """Ошибка - неизвестное действие"""
        self.assertEqual(self.srv.process_for_answer(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """Ошибка -  запрос не содержит штампа времени"""
        self.assertEqual(self.srv.process_for_answer({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(self.srv.process_for_answer({ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не 'Guest'"""
        self.assertEqual(self.srv.process_for_answer(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(self.srv.process_for_answer(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
