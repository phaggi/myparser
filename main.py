import re
from pprint import pprint


def replace_old_struct(struct):
    changes = {'struct<': 'dict(',
               'array<': 'list(',
               '>': ')',
               ':': ': ',
               ',': ', '}
    for key in changes:
        struct = struct.replace(key, changes[key])
    return struct


def set_mark(struct, patterns):
    for pattern in patterns:
        regex = re.compile(pattern)
        words = set(regex.findall(struct))
        for word in words:
            repl = f"'{word}'"
            struct = struct.replace(word, repl)
    return struct


def pair_rbracket(struct: str, rbracket):
    counter = 0
    for number, symbol in enumerate(struct):
        if symbol == '(':
            counter += 1
        elif symbol == ')':
            counter -= 1
        if counter < 0:
            return struct[:number] + rbracket + struct[number + 1:]

def pair_lbracket(struct, lbracket):
    return f'{lbracket}{struct[1:]}'

def pair_brackets(struct, struct_type='dict'):
    changes = {'dict': {'(': '{', ')': '}'},
               'list': {'(': '[', ')': ']'}}
    lbracket = changes[struct_type]['(']
    rbracket = changes[struct_type][')']
    if struct[0] == '(':
        struct = pair_lbracket(struct, lbracket)
        struct = pair_rbracket(struct, rbracket)
    return struct


def set_struct(struct, struct_type):
    structs = struct.split(struct_type, 1)
    structs[1] = pair_brackets(structs[1], struct_type)
    return ''.join(structs)


def replace_struct(struct, struct_type):
    for _ in range(struct.count(struct_type)):
        struct = set_struct(struct, struct_type)
    return struct


if __name__ == '__main__':
    data = ('food',
            'struct<Milk:array<struct<id:string,type:string>>,Oil:string,batter:array<struct<id:string,type:string>>>')
    my_struct = data[1]
    patterns = [r"([\w]+)\:", r"\: ([\w]+)\)"]
    struct = set_mark(replace_old_struct(my_struct), patterns)
    struct_types = ['dict', 'list']
    for struct_type in struct_types:
        struct = replace_struct(struct, struct_type)
    struct = eval(struct)
    pprint(struct)
