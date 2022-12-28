from itertools import islice
from pyparsing import Suppress, Word, Literal, alphanums, OneOrMore, replace_with, srange, Forward

def unescape_token(token):
    return (token.replace('__DOL__', '$')
                 .replace('__OP__', '[')
                 .replace('__CLO__', ']')
                 .replace('__ARO__', '@')
                 .replace('__TIR__', '-')
                 .replace('__PLU__', '+')
                 .replace('__AMP__', '&')
                 .replace('__QUE__', '?')
                 .replace('__COL__', ':'))

def unescape_string(tokens):
    return [unescape_token(token[1:]) for token in tokens]

b64_mapping = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
               'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '*', '%']

def decode_b64(value):
    return sum(b64_mapping.index(char) * (64 ** index)  for index, char in enumerate(value[::-1]))
    
def parse_num(tokens):
    return [decode_b64(token[1:]) for token in tokens]

def parse_negative_num(tokens):
    return [-decode_b64(token[1:]) for token in tokens]

# itertools recipes
def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(islice(it, n))):
        yield batch

def split_nums(value):
    num_digits = decode_b64(value[0])
    return [decode_b64(''.join(digits)) for digits in batched(value[1:], num_digits)]

def parse_num_list(tokens):
    return [split_nums(token[1:]) for token in tokens]

def split_negative_nums(value):
    num_digits = decode_b64(value[0])
    return [-decode_b64(''.join(digits)) for digits in batched(value[1:], num_digits)]

def parse_negative_num_list(tokens):
    return [split_negative_nums(token[1:]) for token in tokens]

undefined = Literal('?').set_parse_action(replace_with(None))
empty_list = Literal(':').set_parse_action(replace_with([]))
a_string = Word('$', alphanums+'_').set_parse_action(unescape_string)
base64chars = srange('[a-zA-Z0-9*%]')
number = Word('@', base64chars).set_parse_action(parse_num)
negative_number = Word('&', base64chars).set_parse_action(parse_negative_num)
number_list = Word('-', base64chars).set_parse_action(parse_num_list)
negative_number_list = Word('+', base64chars).set_parse_action(parse_negative_num_list)
object_value = Forward()

element = a_string | undefined | empty_list | number | negative_number | number_list | negative_number_list | object_value

open_object = Suppress('[')
close_object = Suppress(']')
object_value << open_object + OneOrMore(element) + close_object


BGCDecoder = OneOrMore(element)
