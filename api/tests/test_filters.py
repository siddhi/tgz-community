from datetime import timedelta
import pytest

from api.filters import humanise_timedelta, underscore_to_space

@pytest.mark.parametrize(
    "delta, output", [
    (timedelta(0), "within an hour"),
    (timedelta(hours=1), "1 hour ago"),
    (timedelta(hours=1, minutes=10), "1 hour ago"),
    (timedelta(hours=2, minutes=10), "2 hours ago"),
    (timedelta(days=1), "1 day ago"),
    (timedelta(days=1, minutes=10), "1 day ago"),
    (timedelta(days=2, minutes=10), "2 days ago"),
    (timedelta(days=5), "5 days ago"),
])
def test_humanise(delta, output):
    assert humanise_timedelta(delta) == output

def test_underscore_to_space():
    assert underscore_to_space("a_b_c_d") == 'a b c d'
