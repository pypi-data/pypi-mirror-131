"""Декораторы"""

import sys
import logging
import socket
import project_logs.configs.server_log_config
import project_logs.configs.client_log_config
import traceback
import inspect

# Метод определения модуля, источника запуска.
if sys.argv[0].find('client.py') == -1:
    # если не клиент то сервер!
    LOGGER = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client')


# Реализация в виде функции
def log(func_to_log):
    """Функция-декоратор"""

    def log_saver(*args, **kwargs):
        LOGGER.debug(
            f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. '
            f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret

    return log_saver


# Реализация в виде класса
class Log:
    """Класс-декоратор"""

    def __call__(self, func_to_log):
        def log_saver(*args, **kwargs):
            """Обертка"""
            result = func_to_log(*args, **kwargs)
            LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                         f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                         f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
            return result

        return log_saver


def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортировать необходимо тут, иначе ошибка рекурсивного импорта.
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
