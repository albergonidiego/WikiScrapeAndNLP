import datetime
import json
# import os
# *********************************************************************************************************************
# TOOLS

# Reusable function to save json responses
def salva_json (data, json_filename):
    json_datetime_now = datetime.datetime.now()
    json_datetime_now_usable = json_datetime_now.strftime("%Y%m%d%H%M%S")

    filename = json_datetime_now_usable + "_" + json_filename + ".json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return filename

def salva_txt (data, txt_filename):
    data_to_write = remove_blank_lines(data)
    txt_datetime_now = datetime.datetime.now()
    txt_datetime_now_usable = txt_datetime_now.strftime("%Y%m%d%H%M%S")

    filename = txt_datetime_now_usable + "_"
    filename = filename + txt_filename + ".txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data_to_write)

    return filename

def salva_dict (dict, txt_filename):
    txt_datetime_now = datetime.datetime.now()
    txt_datetime_now_usable = txt_datetime_now.strftime("%Y%m%d%H%M%S")

    dict = json.dumps(dict, sort_keys=True, indent=4)
    filename = "_" + txt_datetime_now_usable
    filename = txt_filename + filename + ".txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(dict)

    return filename

def remove_blank_lines (data):
    # text = os.linesep.join([s for s in data.splitlines() if s])
    if data.startswith('\n'):
        data.replace(data[:2], '')
    text = data.replace('\n\n', '\n')
    return text

def remove_things_in_sq_brackets (data):
    # Removes squared brackets and anything in it
    # Reworked from code created by pradyunsg
    # https://stackoverflow.com/questions/14596884/remove-text-between-and-in-python
    ret = ''
    skip1c = 0
    for i in data:
        if i == '[':
            skip1c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif skip1c == 0:
            ret += i
    return ret

def array_it (data):
    array = []
    for item in data:
        array.append(item)
    return array
