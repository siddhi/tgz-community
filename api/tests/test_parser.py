from api.parser import BGCDecoder

def test_parse_single_token():
    output = BGCDecoder.parse_string('$player1')
    assert list(output) == ['player1']

def test_parse_multiple_tokens():
    output = BGCDecoder.parse_string('$player1$player2')
    assert list(output) == ['player1', 'player2']

def test_string_unescape():
    output = BGCDecoder.parse_string('$__DOL____OP____CLO____ARO____TIR____PLU____AMP____QUE____COL__')
    assert list(output) == ['$[]@-+&?:']

def test_empty_list():
    output = BGCDecoder.parse_string(':')
    assert list(output) == [[]]

def test_undefined():
    output = BGCDecoder.parse_string('?')
    assert list(output) == [None]
    
def test_number():
    output = BGCDecoder.parse_string('@1')
    assert list(output) == [1]
    
def test_multidigit_number():
    output = BGCDecoder.parse_string('@1O')
    assert list(output) == [114]
    
def test_negative_number():
    output = BGCDecoder.parse_string('&1O')
    assert list(output) == [-114]

def test_single_digit_num_list():
    output = BGCDecoder.parse_string('-1123')
    assert list(output) == [[1, 2, 3]]

def test_multi_digit_num_list():
    output = BGCDecoder.parse_string('-2131O')
    assert list(output) == [[67, 114]]

def test_negative_num_list():
    output = BGCDecoder.parse_string('+2131O')
    assert list(output) == [[-67, -114]] 

def test_object():
    output = BGCDecoder.parse_string('[$player1@2@6??@3?]')
    assert list(output) == ['player1', 2, 6, None, None, 3, None]

