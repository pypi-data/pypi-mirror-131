import jieba
import pinyiniser
import os
from pathlib import Path

curr_dir = '\\'.join(pinyiniser.__file__.split('\\')[0:-1])
numeric_dict = os.path.join(curr_dir, Path('./data/cedict_ts_no_space_numerals.u8'))
diacritic_dict = os.path.join(curr_dir, Path('./data/cedict_ts_pinyin.u8'))

do_not_parse_set = {'？', '，', '！', '。', '；', '“', '”', '：', '–', '—', '＊',
        '…', '、', '～', '－', '（', '）', '─', '＜', '＞', '．', '《', '》',
        '％', '·', '<', '>', '’', '‘', '+', '/', '~', '!', '@', '#', '$',
        '%', '^', '&', '*', '(', ')', '_', '-', '=', '\\', '{', '}', '|', ';',
        '\'', '"', ',', '.'}

def write_lines(lines, path):
    with open(path, 'w+') as f:
        i = 1
        for line in lines:
            f.write('Line ' + str(i) + ':\n')
            f.write(line)
            i += 1
        f.write('Line ' + str(i) + ':\n')

def read_lines(path):
    with open(path, 'r') as f:
        lines = []
        string_to_add = ''
        first = True
        for line in f.readlines():
            if 'Line' in line:
                if first:
                    first = False
                    continue
                lines.append(string_to_add)
                string_to_add = ''
            else:
                string_to_add += line
    return lines
        
def add_pinyin(zh_string, zh_dict, special_pinyin={},
        do_not_parse=do_not_parse_set):
    if zh_string in special_pinyin:
        return zh_string + '\n' + special_pinyin[zh_string] + '\n'
    
    pinyin = get_pinyin(zh_string, zh_dict, do_not_parse)
    zh_string += '\n'
    first = True 
    for item in pinyin:
        if item in do_not_parse or first:
            zh_string += item
            first = False
        else:
            zh_string += ' ' + item

    return zh_string + '\n'

def get_pinyin(zh_string, zh_dict, do_not_parse):
    line_segs = tuple(jieba.cut(zh_string, cut_all=False))
    pinyin = []
    for word in line_segs:
        if word in zh_dict:
            pinyin.append(zh_dict[word]['pinyin'])
        else:
            if word in do_not_parse or ord(word[0]) < 255:
                pinyin.append(word)
            else: 
                for character in word:
                    if character in zh_dict:
                        pinyin.append(zh_dict[character]['pinyin'])
                    else:
                        pinyin.append(character)

    return pinyin

def get_dictionary(numeric=False):
    if numeric == True:
        return parse_dict(numeric_dict)
    return parse_dict(diacritic_dict)

def parse_dict(path):
    return cc_cedict_parser.parse_dict(path)

if __name__ == '__main__':
    from data import cc_cedict_parser
    print(diacritic_dict)
else:
    from .data import cc_cedict_parser
