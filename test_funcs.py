import pytest

import numpy as np

from funcs import rgb2hex


@pytest.mark.parametrize('rgb,output', [
    ([255, 0, 0], '#ff0000'),
    ([0, 255, 0], '#00ff00'),
    ([0, 0, 255], '#0000ff')
])
def test_rgb2hex(rgb, output):
    """Test translation or rgb to hex representation"""
    assert rgb2hex(rgb) == output
