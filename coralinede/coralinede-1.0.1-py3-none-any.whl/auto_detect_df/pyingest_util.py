import os
import re
from operator import itemgetter


def get_clean_col_and_delimiter(file_path):
    """
    detect delimiter in text file by glancing at first row
    :param file_path: path of text file (str)
    :return:
        number of delimiters that are detected (int)
        delimiter (str)
    """

    first_line = None
    with open(file_path, encoding='utf8') as file:
        first_line = file.readline()

    list_of_count_delimiters = [
        (',', first_line.count(',')),
        ('|', first_line.count('|')),
        ('\t', first_line.count('\t'))
    ]

    delimiter = max(list_of_count_delimiters, key=itemgetter(1))[0]

    arr_header = get_simplify_column_name(first_line, delimiter)

    return arr_header, delimiter


def get_simplify_column_name(column_name, delimiter):
    """
    simplify all the column name by removing all non-alphabetic character 
    except number, and converting name into snake case
    :param column_name: column name (str)
    :param deliemter: delimiter that detected from detect_delimiter() (str)
    :return:
    array of preprocessed column name (array)
    """

    temp_string = column_name.lower()
    arr_header = re.sub('[^{}_A-Za-z0-9 ]+'.format(delimiter), '', temp_string).replace(' ', '_').split(delimiter)

    return arr_header