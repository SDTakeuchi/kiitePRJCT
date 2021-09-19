import re

def regex_get_first_number(string):
    return re.findall('[0-9]+', string)[0]

def regex_get_numbers(string):
    return re.findall('[0-9]+', string)

def truncate(string, length, ellipsis='...'):
    return string[:length] + (ellipsis if string[length:] else '')