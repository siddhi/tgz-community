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

