#!/usr/bin/env python3
""" Regexing Module """
import re

def filter_datum(fields, redaction, message, separator):
    regex_pattern = r'({})'.format('|'.join(map(re.escape, fields)))
    return re.sub(regex_pattern, redaction, message)

