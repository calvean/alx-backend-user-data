#!/usr/bin/env python3
""" Regexing Module """
import re
from typing import List


def filter_datum(
  fields: List[str],
  redaction: str,
  message: str,
  separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Arguments:
        fields: list of strings representing fields to obfuscate.
        redaction: string representing value to replace
        message: string representing the log line.
        separator: string separating the fields in the log line.

    Returns:
        The obfuscated log message.
    """
    regex_pattern = r'({})'.format('|'.join(map(re.escape, fields)))
    obfuscated_message = re.sub(regex_pattern, redaction, message)

    return obfuscated_message
