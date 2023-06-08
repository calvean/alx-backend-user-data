#!/usr/bin/env python3
""" Regexing Module """
import re
from typing import List
import logging
import mysql.connector
from os import getenv


PII_FIELDS: List[str] = ['name', 'email', 'phone', 'ssn', 'password']


def filter_datum(
  fields: List[str],
  redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields: A list of strings for fields to obfuscate.
        redaction: A string for value to replace fields with.
        message: A string representing the log line.
        separator: A string for character separating fields in log line.

    Returns:
        The obfuscated log message.
    """
    for field in fields:
        message = re.sub(
          rf"{field}=.*?{separator}",
          rf"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Custom log formatter that redacts sensitive information.
    """

    REDACTION: str = "***"
    FORMAT: str = "[HOLBERTON] %(name)s \
    %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR: str = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record and redacts sensitive information.

        Args:
            record: The log record to format.

        Returns:
            The formatted log message with redacted sensitive information.
        """
        return filter_datum(
          self.fields,
          self.REDACTION,
          super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Retrieves a logger with redaction of sensitive information.

    Returns:
        A Logger object with redaction enabled.
    """
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False

    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Retrieves a connection to the secure Holberton database.

    Returns:
        A MySQLConnection object representing the database connection.
    """
    connection_db = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME'))

    return connection_db


def main():
    """
    Retrieves data from the users table
    and logs it with redaction of sensitive information.
    """
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    log = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(str_row.strip())

    cursor.close()
    database.close()


if __name__ == '__main__':
    main()
