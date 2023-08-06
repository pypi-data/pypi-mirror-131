"""Only gets pinyin"""
import sys

#define functions

#builds a dictionary with a simp character as the key
#the key accesses a dictionary of attributes - pinyin only in this case
#dictionary[key]['pinyin'] accesses a list
def parse_lines(lines):
    dictionary = {}
    for line in lines:
        parts = get_parts_of_line(line)
        add_entry(parts, dictionary)
    
    return dictionary

def get_parts_of_line(line):
    parts = {}
    chinese, english = line.split('/', 1)
    if chinese in skip:
        return ''
    trad, simp, pinyin = chinese.split(' ', 2)
    pinyin = prep_pinyin(pinyin)

    parts[simp.strip()] = {'pinyin': pinyin}
    parts[trad.strip()] = {'pinyin': pinyin}
    
    return parts

def prep_pinyin(pinyin):
    return pinyin.strip('[] ').lower()
    
#no return deliberately
def add_entry(parts, dictionary):
    for key in parts:
        if key not in dictionary:
            dictionary[key] = parts[key]

def parse_dict(path):
    #make each line into a dictionary
    with open(path, 'r') as f:
        lines = f.readlines()
        return parse_lines(lines)

if __name__ == "__main__":
    from pinyin_skip import skip
else:
    from .pinyin_skip import skip
