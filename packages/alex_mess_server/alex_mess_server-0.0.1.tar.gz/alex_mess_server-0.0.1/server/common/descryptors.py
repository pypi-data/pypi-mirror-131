import ipaddress
import logging
import sys

# Инициализация логера
# метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    logger = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client')


# Дескриптор для описания порта:
class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Address:
    def __set__(self, instance, value):
        # value - 127.0.0.1
        # Попытка преобразовать адрес в объект IPv4
        try:
            ipv4 = ipaddress.IPv4Address(value)
            # Попытка не удачная, тогда получаем исключение
        except ipaddress.AddressValueError:
            logger.critical(f'Попытка запуска сервера с адресом не соответствущем IPv4 - {value}')
            exit(1)

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # name - host
        self.name = name
