import sys
import os
import pytest
import numpy as np

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.LEC_2_Floating_Point_Explorer import float_to_bin_and_decimal, float_to_bin, format_bits

def test_format_bits():
    assert format_bits("1111000011110000", 4) == "1111 0000 1111 0000"
    assert format_bits("101", 4) == "101"
    assert format_bits("10101010", 2) == "10 10 10 10"

# --- Tests for float_to_bin ---

def test_float_to_bin_float16():
    # Test with a simple value
    b, s, e, m = float_to_bin(0.1, "float16")
    assert b == "0010111001100110"
    assert s == 1
    assert e == 5
    assert m == 10

def test_float_to_bin_bfloat16():
    # Test with a simple value
    b, s, e, m = float_to_bin(0.1, "bfloat16")
    assert b == "0011110111001101" # Rounded from float32
    assert s == 1
    assert e == 8
    assert m == 7

def test_float_to_bin_float32():
    # Test with a simple value
    b, s, e, m = float_to_bin(0.1, "float32")
    assert b == "00111101110011001100110011001101"
    assert s == 1
    assert e == 8
    assert m == 23

# --- Tests for float_to_bin_and_decimal ---

# Test cases for various numbers and types
@pytest.mark.parametrize("value, dtype, expected_bin, expected_dec", [
    # Float16
    (1.0, "float16", "0011110000000000", 1.0),
    (-2.5, "float16", "1100000100000000", -2.5),
    (0.1, "float16", "0010111001100110", np.float16(0.1)),
    (65504, "float16", "0111101111111111", 65504.0), # Max float16
    # Bfloat16
    (1.0, "bfloat16", "0011111110000000", 1.0),
    (-2.5, "bfloat16", "1100000000100000", -2.5),
    (0.1, "bfloat16", "0011110111001101", 0.10009765625), # Rounded value
    # Float32
    (1.0, "float32", "00111111100000000000000000000000", 1.0),
    (-2.5, "float32", "11000000001000000000000000000000", -2.5),
    (0.1, "float32", "00111101110011001100110011001101", np.float32(0.1)),
])
def test_float_to_bin_and_decimal_regular(value, dtype, expected_bin, expected_dec):
    b, s, e, m, dec = float_to_bin_and_decimal(value, dtype)
    assert b == expected_bin
    assert np.isclose(dec, expected_dec)

# --- IEEE 754 Special Cases ---

@pytest.mark.parametrize("value, dtype, expected_bin, expected_dec_repr", [
    # Positive Zero
    (0.0, "float16", "0000000000000000", 0.0),
    (0.0, "bfloat16", "0000000000000000", 0.0),
    (0.0, "float32", "00000000000000000000000000000000", 0.0),
    # Negative Zero
    (-0.0, "float16", "1000000000000000", -0.0),
    (-0.0, "bfloat16", "1000000000000000", -0.0),
    (-0.0, "float32", "10000000000000000000000000000000", -0.0),
    # Positive Infinity
    (float('inf'), "float16", "0111110000000000", float('inf')),
    (float('inf'), "bfloat16", "0111111110000000", float('inf')),
    (float('inf'), "float32", "01111111100000000000000000000000", float('inf')),
    # Negative Infinity
    (float('-inf'), "float16", "1111110000000000", float('-inf')),
    (float('-inf'), "bfloat16", "1111111110000000", float('-inf')),
    (float('-inf'), "float32", "11111111100000000000000000000000", float('-inf')),
])
def test_float_to_bin_and_decimal_special_values(value, dtype, expected_bin, expected_dec_repr):
    b, s, e, m, dec = float_to_bin_and_decimal(value, dtype)
    assert b == expected_bin
    if np.isinf(dec):
        assert np.isinf(expected_dec_repr) and np.sign(dec) == np.sign(expected_dec_repr)
    else:
        assert np.isclose(dec, expected_dec_repr) and np.sign(dec) == np.sign(expected_dec_repr)

# NaN is special because the mantissa can vary, and NaN != NaN
@pytest.mark.parametrize("dtype, sign_len, exp_len", [
    ("float16", 1, 5),
    ("bfloat16", 1, 8),
    ("float32", 1, 8),
])
def test_float_to_bin_and_decimal_nan(dtype, sign_len, exp_len):
    value = float('nan')
    b, s, e, m, dec = float_to_bin_and_decimal(value, dtype)
    
    # Check for NaN properties
    assert np.isnan(dec)
    
    # For NaN, exponent must be all 1s
    exponent_bits = b[sign_len : sign_len + exp_len]
    assert exponent_bits == '1' * exp_len
    
    # For NaN, mantissa must be non-zero
    mantissa_bits = b[sign_len + exp_len:]
    assert '1' in mantissa_bits
