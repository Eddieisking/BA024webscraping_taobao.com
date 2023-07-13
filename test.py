"""
# Project:
# Author: Eddie
# Date: 
"""

import re

def extract_number(string):
    number = re.findall(r'\d+', string)
    if number:
        return int(number[0])
    else:
        return 0

s = '有用（-1）'
d = extract_number(s)
print(d)
print(type(d))