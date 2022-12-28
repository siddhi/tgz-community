from pyparsing import Word, Suppress, alphanums, OneOrMore

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

a_string = Word('$', alphanums+'_').set_parse_action(unescape_string)

element = a_string

BGCDecoder = OneOrMore(element)
