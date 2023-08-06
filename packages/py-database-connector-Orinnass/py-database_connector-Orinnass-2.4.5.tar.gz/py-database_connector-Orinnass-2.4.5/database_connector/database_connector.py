"""
Модуль с классами подключения к бд
"""
from tools import Singleton
from time import sleep
from threading import Thread
# TODO: Обновить библиотеку как появится новая версия
from pymysqlpool.pool import Pool
import pymysql
from pymysql.cursors import DictCursor
from config import Configuration
from typing import Union, Optional, List, Dict


class Connection:
    """
    Класс подключения к бд
    """
    def __init__(self, connection: pymysql.Connection, pool_connections):
        config = Configuration()
        self.__logger = config.logging.get_logger(__name__)
        self.__logger.debug(f'Получено подключение к бд {connection}')
        self.__connection: pymysql.Connection = connection
        self.__pool: ConnectionsPool = pool_connections
        del config

    def __del__(self):
        self.release()

    def release(self):
        """
        Возвращение подключения в пул
        """
        if self.__connection:
            self.__pool.release(self.__connection)
            self.__logger.debug(f'Возвращение подключения в пул {self.__connection}')
            self.__connection = None

    def select(self, table: str, columns: List[str] = '*', joins: List[Dict[str, str]] = None,
               where: str = None) -> Optional[list]:
        """
        Метод для запроса select
        """
        query = "SELECT "
        if type(columns) == 'list':
            for i in columns:
                query += f"{i} "
        else:
            query += f"{columns} "

        query += f"FROM {table}"
        if joins:
            for i in joins:
                query += f"{' ' + i['type'] + ' ' if i.get('type') else ' '} JOIN " \
                         f"`{i['table']}` ON `{i['table']}`.`{i['join_column']}` = `{table}`.`{i['join_table_column']}`"

        if where:
            query += f" WHERE {where}"

        return self.custom_sql(query)

    def insert(self, table: str, value_columns: List[Dict[str, str]], where: str = None) -> int:
        """
        Метод для выполнения запроса insert
        """
        query = f'INSERT INTO {table} '

        columns = ''
        values = ''
        for i in value_columns:
            columns += f"{i['column']},"
            values += f"{i['value']},"
        query += f"({columns[:-1]}) VALUES ({values[:-1]})"

        if where:
            query += f" WHERE {where}"

        return self.custom_sql(query)

    def custom_sql(self, sql: str) -> Union[int, list]:
        """
        Метод для выполнения самописного sql запроса
        """
        cursor = self.__connection.cursor(DictCursor)
        try:
            self.__logger.debug(f"Выполнение запроса: {sql}", stack_info=True, stacklevel=2)
            cursor.execute(sql)
            if cursor.lastrowid:
                self.__logger.debug(f'Выполнен запрос на изменение базы.\n'
                                    f'{cursor.lastrowid=}')
                return cursor.lastrowid
            else:
                data = cursor.fetchall()
                self.__logger.debug(f'Выполнен запрос на получение данных из базы.\n'
                                    f'{data=}')
                return data
        except Exception as e:
            self.__logger.error(str(e), exc_info=True, stack_info=True)
            raise
        finally:
            cursor.close()


class ConnectionsPool(metaclass=Singleton):
    """Класс управления подключений базы"""

    def __init__(self):
        config = Configuration()
        self.__logger = config.logging.get_logger(__name__)
        self.__logger.debug('Создание пула конектов к БД')
        connection_args = {}
        if config.DB.get('args'):
            for i in config.DB.get('args').keys():
                connection_args[i] = config.DB['args'][i]
        self.__pool = Pool(host=config.DB['host'], user=config.DB["user"],
                           password=config.DB['password'], db=config.DB['DB_name'],
                           port=config.DB["port"], autocommit=True, ping_check=True,
                           max_size=config.DB['max_connections'], min_size=config.DB['min_connections'],
                           **connection_args)

        self.__logger.debug(f'Создан пул конектов к БД {self.__pool}')
        self.__logger.debug('Инициализация пула конектов к БД')
        self.__pool.init()

        if config.DB["ping_connection"]["enabled"]:
            self.__cron_ping_connections = Thread(target=self.__ping_connections__, daemon=True)
            self.__ping_interval = config.DB["ping_connection"]["interval"]
            self.__cron_ping_connections.start()
        del config

    def __del__(self):
        self.close()

    def __ping_connections__(self):
        self.__logger.info(f"Запуск крона для пинга конектов")
        while True:
            connections = []
            while self.__pool.unuse_list:
                connections.append(self.__pool.get_conn())
            self.__logger.debug(f"Получены конекты для пинга: {connections}")
            for i in connections:
                cursor_connection = i.cursor()
                cursor_connection.execute("SELECT 'ping'")
                cursor_connection.close()
                self.__pool.release(i)
            sleep(self.__ping_interval)

    def close(self):
        """Метод закрытия подключений"""
        self.__pool.destroy()

    def get_connection(self) -> Connection:
        """
        Метод получения конекта из пула
        """
        try:
            self.__logger.debug(f'Размер пула: {self.__pool.current_size}\n'
                                f'Используемые подключения: {self.__pool.inuse_list}\n'
                                f'Неиспользуемые подключения: {self.__pool.unuse_list}')
            mysql_connection = self.__pool.get_conn()
            self.__logger.debug(f"Получено подключение {mysql_connection}")
            connection = Connection(mysql_connection, self.__pool)
            return connection
        except Exception as e:
            self.__logger.error(str(e), exc_info=True)
            raise

    def release(self, connection):
        """
        Метод возврата конекта в пул
        """
        self.__pool.release(connection)
        self.__logger.debug(f'Подключение возвращено в пул {connection}')
