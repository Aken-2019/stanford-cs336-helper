def float_to_bin_and_decimal(value, dtype):
	import numpy as np
	if dtype == "float16":
		f = np.float16(value)
		b = np.binary_repr(np.frombuffer(f.tobytes(), dtype=np.uint16)[0], width=16)
		return b, 1, 5, 10, float(f)
	elif dtype == "bfloat16":
		# bfloat16 (Brain Float 16): 1 sign bit, 8 exponent bits, 7 mantissa bits
		# It's essentially the upper 16 bits of a float32 representation
		
		# Step 1: Convert input to float32 to get the full 32-bit representation
		f = np.float32(value)
		
		# Step 2: Extract the 32-bit integer representation
		# np.frombuffer reads the float32 bytes as a uint32 integer
		as_int = np.frombuffer(f.tobytes(), dtype=np.uint32)[0]
		
		# Step 3: Apply "Round to nearest, ties to even" rounding rule
		# Extract the upper 16 bits and the bit that determines rounding
		upper_16_bits = int((as_int >> 16) & 0xFFFF)  # Convert to Python int
		lower_16_bits = int(as_int & 0xFFFF)         # Convert to Python int
		
		# The rounding bit is the most significant bit of the lower 16 bits (bit 15)
		rounding_bit = (lower_16_bits >> 15) & 1
		
		# For "ties to even": if rounding bit is 1, we need to check:
		# 1. If there are any bits set in the remaining 15 bits (not a tie)
		# 2. If it's a tie, round to make the result even (LSB of upper 16 bits = 0)
		if rounding_bit == 1:
			# Check if this is a tie (only the rounding bit is set in lower 16 bits)
			remaining_bits = lower_16_bits & 0x7FFF  # Lower 15 bits
			is_tie = (remaining_bits == 0)
			
			if not is_tie:
				# Not a tie, round up
				upper_16_bits += 1
			elif is_tie and (upper_16_bits & 1) == 1:
				# It's a tie and current result is odd, round up to make it even
				upper_16_bits += 1
			# If it's a tie and current result is even, don't round (keep it even)
		
		# Handle overflow (though rare for typical values)
		bfloat_int = upper_16_bits & 0xFFFF
		
		# Step 4: Generate binary representation string for display
		b = np.binary_repr(bfloat_int, width=16)
		
		# Step 5: Reconstruct the decimal value from bfloat16
		# The key insight: bfloat16 is just float32 with lower 16 bits set to zero
		# So we reconstruct by shifting the 16-bit value back to upper position
		reconstructed_int = bfloat_int << 16  # Shift left 16 positions, lower bits become 0
		
		# Step 6: Convert the reconstructed integer back to float32
		# Use the same byte order as the original float32 representation
		reconstructed_bytes = reconstructed_int.to_bytes(4, byteorder='little')
		dec = float(np.frombuffer(reconstructed_bytes, dtype=np.float32)[0])
		
		return b, 1, 8, 7, dec
	elif dtype == "float32":
		# Convert to float32 to get the exact representation stored
		f = np.float32(value)
		packed = struct.pack('>f', f)
		as_int = struct.unpack('>I', packed)[0]
		b = f"{as_int:032b}"
		# Return the exact float32 value, not the original input
		return b, 1, 8, 23, float(f)
	else:
		return None, None, None, None, None

import streamlit as st
import struct

st.title("🔢 IEEE 754 Floating-Point Explorer")
st.write("Interactive tool to explore floating-point representations, precision, and range across different formats: float16, bfloat16, and float32.")
st.markdown("""
Under the converter section, you can also find explanations about the IEEE 754 standard and how bfloat16 is derived from float32.
""")
st.markdown("---")

def format_bits(bits, group=4):
	# Insert space after every 'group' bits

	return ' '.join([bits[i:i+group] for i in range(0, len(bits), group)])

def float_to_bin(value, dtype):
	if dtype == "float16":
		import numpy as np
		# IEEE 754 half precision: 1 sign, 5 exponent, 10 mantissa bits
		f = np.float16(value)
		b = np.binary_repr(np.frombuffer(f.tobytes(), dtype=np.uint16)[0], width=16)
		return b, 1, 5, 10
	elif dtype == "bfloat16":
		import numpy as np
		# bfloat16: 1 sign, 8 exponent, 7 mantissa bits
		# Extract upper 16 bits from float32 representation with proper rounding
		f = np.float32(value)
		as_int = np.frombuffer(f.tobytes(), dtype=np.uint32)[0]
		
		# Apply "Round to nearest, ties to even" rounding rule
		upper_16_bits = int((as_int >> 16) & 0xFFFF)  # Convert to Python int
		lower_16_bits = int(as_int & 0xFFFF)         # Convert to Python int
		rounding_bit = (lower_16_bits >> 15) & 1
		
		if rounding_bit == 1:
			remaining_bits = lower_16_bits & 0x7FFF
			is_tie = (remaining_bits == 0)
			
			if not is_tie:
				upper_16_bits += 1
			elif is_tie and (upper_16_bits & 1) == 1:
				upper_16_bits += 1
		
		bfloat_int = upper_16_bits & 0xFFFF
		b = np.binary_repr(bfloat_int, width=16)
		return b, 1, 8, 7
	elif dtype == "float32":
		# IEEE 754 single precision: 1 sign, 8 exponent, 23 mantissa bits
		packed = struct.pack('>f', value)
		as_int = struct.unpack('>I', packed)[0]
		b = f"{as_int:032b}"
		return b, 1, 8, 23
	else:
		return None, None, None, None


types = ["float16", "bfloat16", "float32"]
selected_types = st.multiselect("Select float types to compare", types, default=["float16", "bfloat16", "float32"])
value = st.number_input("⭐ Enter a number to explore ⭐", value=0.1, format="%f", key="main_value")

rows = []
for dtype in selected_types:
	# Use the same value for all types, but assign a unique key for each input if you want per-type input
	bits, sign_len, exp_len, mant_len, dec_value = float_to_bin_and_decimal(value, dtype)
	if bits:
		sign = bits[:sign_len]
		exponent = bits[sign_len:sign_len+exp_len]
		mantissa = bits[sign_len+exp_len:]
		
		# Format decimal with appropriate precision for each type
		if dtype == "float32":
			# Show up to 27 significant digits for float32 (sufficient for exact representation)
			decimal_str = f"{dec_value:.27g}"
		elif dtype == "float16":
			# Show up to 13 significant digits for float16
			decimal_str = f"{dec_value:.13g}"
		elif dtype == "bfloat16":
			# Show up to 11 significant digits for bfloat16
			decimal_str = f"{dec_value:.11g}"
		else:
			decimal_str = f"{dec_value}"
		
		rows.append({
			"Type": dtype,
			"Decimal": decimal_str,
			"Sign": format_bits(sign),
			"Exponent": format_bits(exponent),
			"Mantissa": format_bits(mantissa),
			"Raw bits": format_bits(bits, 4)
		})
	else:
		rows.append({
			"Type": dtype,
			"Decimal": "Error",
			"Sign": "-",
			"Exponent": "-",
			"Mantissa": "-",
			"Raw bits": "-"
		})

if rows:
	st.subheader("Binary Representation Comparison")
	st.table(rows)
st.markdown("---")


# IEEE 754 Floating-Point Formula
st.markdown("### 📐 IEEE 754 Floating-Point Formula")
st.markdown("""
The decimal value of a floating-point number is calculated using the following formula:
""")

st.latex(r"""
\text{Value} = (-1)^{\text{sign}} \times 2^{(\text{exponent} - \text{bias})} \times (1 + \text{mantissa})
""")

st.markdown("""
Where:
- **Sign bit**: 0 = positive, 1 = negative
- **Exponent**: Binary representation, biased by a constant
- **Mantissa** (Significand): Fractional part, with implicit leading 1
- **Bias values**: 
  - float16: 15 (2^(5-1) - 1)
  - bfloat16: 127 (2^(8-1) - 1)  
  - float32: 127 (2^(8-1) - 1)

**Example**: For a positive number with exponent bits `10000010` and mantissa `01000000000000000000000` in float32:
- Sign = 0 (positive)
- Exponent = 130 (binary 10000010), so 130 - 127 = 3
- Mantissa = 0.25 (binary 0.01), so 1 + 0.25 = 1.25
- Result = (+1) × 2³ × 1.25 = 8 × 1.25 = 10.0
""")

st.markdown("---")

# Educational section about bfloat16
st.markdown("### 🧠 Understanding bfloat16 (Brain Float 16)")
st.markdown("""
**Key Insight**: bfloat16 is simply the upper 16 bits of float32 - to reconstruct the decimal value, 
we just need to shift those 16 bits back to their original position and zero out the lower 16 bits.

**Why bfloat16?**
- Designed by Google for machine learning applications
- Maintains the same exponent range as float32 (8 bits) but reduces mantissa precision (7 bits vs 23 bits)
- This makes it ideal for neural networks where gradient magnitude is more important than precision

**Format Comparison:**
- **float32**: 1 sign + 8 exponent + 23 mantissa = 32 bits
- **bfloat16**: 1 sign + 8 exponent + 7 mantissa = 16 bits (upper half of float32)
- **float16**: 1 sign + 5 exponent + 10 mantissa = 16 bits (different format)
""")

st.markdown("#### 📏 Range vs Precision: How It's Reflected in the IEEE 754 Equation")
st.latex(r"""
\text{Value} = (-1)^{\text{sign}} \times 2^{(\text{exponent} - \text{bias})} \times (1 + \text{mantissa})
""")

st.markdown(r"""

**Range** refers to the **magnitude** or **scale** of numbers that can be represented - from the tiniest values near zero to the largest values before infinity. It determines "how big" or "how small" a number can be.
In the above equation, the exponent term $2^{(\text{exponent} - \text{bias})}$ determines the scale of the number (e.g., 10^-10 in decimal).
			
**Precision** refers to the **exactness** or **granularity** of the representation - how many distinct values can be represented between any two consecutive powers of 2. It determines "how accurately" a number can be stored.
In the equation, the mantissa term $(1 + \text{mantissa})$ determines the fractional part of the number (e.g., 1.2345 in decimal).

The combination of exponent and mantissa defines the overall representation of floating-point numbers. (e.g., 1.2345 × 10^-10 in decimal).
			
	
**Range Analysis:**
- **bfloat16**: 8-bit exponent → range ≈ $2^{-126}$ to $2^{+127}$ (same as float32)
- **float16**: 5-bit exponent → range ≈ $2^{-14}$ to $2^{+15}$ (much smaller)
- **float32**: 8-bit exponent → range ≈ $2^{-126}$ to $2^{+127}$

**Precision Analysis:**
- **bfloat16**: 7-bit mantissa → $2^7 = 128$ possible fractional values → ~3-4 decimal digits
- **float16**: 10-bit mantissa → $2^{10} = 1024$ possible fractional values → ~3-4 decimal digits  
- **float32**: 23-bit mantissa → $2^{23} = 8.4M$ possible fractional values → ~7 decimal digits

""")


st.markdown(r"""
**Key Takeaways:**
1. **Same Range**: bfloat16 and float32 can represent the same magnitude of numbers (tiny to huge) because they share the same 8-bit exponent
2. **Lower Precision**: bfloat16 has fewer distinct values between any two powers of 2 because of the shorter 7-bit mantissa
3. **ML Advantage**: Neural networks care more about gradient magnitude (range) than exact values (precision), making bfloat16 ideal
4. **Memory Efficiency**: Half the bits of float32 while maintaining the critical range for deep learning
""")


st.markdown("#### ⚙️ How bfloat16 is Derived from float32")
st.markdown("""
**Conversion Process:**
1. Convert input to float32 representation
2. Extract the upper 16 bits with proper rounding
3. **Rounding Rule**: "Round to nearest, ties to even" (banker's rounding)
   - If the bit being rounded is 1 and there are other bits set, round up
   - If it's exactly a tie (only the rounding bit is 1), round to make the result even
   - This minimizes bias in repeated calculations
4. To get decimal back: shift those 16 bits left by 16 positions, filling lower bits with zeros
""")

st.markdown("""
**Rounding Example**: 
- Original float32 bits: `0 01111111 01000000000000100000000`
- Upper 16 bits: `0011111110100000`, Lower 16: `0000000100000000` 
- Rounding bit (bit 15 of lower): 1, Remaining bits: non-zero
- Result: Round up → `0011111110100001` (since remaining bits are non-zero)
""")

st.markdown("---")

# Special IEEE 754 Values Section
st.markdown("### 🔍 IEEE 754 Special Values")
st.markdown("""
IEEE 754 defines special bit patterns for representing infinity, NaN (Not a Number), and zero values.
These special cases are determined by the exponent and mantissa bit patterns:
""")

import math

# Define special values for each type
special_cases = {
    "Positive Zero": (0.0, "All exponent bits = 0, all mantissa bits = 0"),
    "Negative Zero": (-0.0, "Sign = 1, all exponent bits = 0, all mantissa bits = 0"),
    "Positive Infinity": (float('inf'), "All exponent bits = 1, all mantissa bits = 0"),
    "Negative Infinity": (float('-inf'), "Sign = 1, all exponent bits = 1, all mantissa bits = 0"),
    "NaN (Not a Number)": (float('nan'), "All exponent bits = 1, any mantissa bits ≠ 0")
}

special_rows = []
for case_name, (value, description) in special_cases.items():
    for dtype in ["float32"]:
        try:
            bits, sign_len, exp_len, mant_len, dec_value = float_to_bin_and_decimal(value, dtype)
            if bits:
                sign = bits[:sign_len]
                exponent = bits[sign_len:sign_len+exp_len]
                mantissa = bits[sign_len+exp_len:]
                
                # Special formatting for special values
                if math.isnan(dec_value):
                    decimal_str = "NaN"
                elif math.isinf(dec_value):
                    decimal_str = "+∞" if dec_value > 0 else "-∞"
                elif dec_value == 0.0:
                    # Distinguish positive and negative zero
                    if math.copysign(1.0, dec_value) == 1.0:
                        decimal_str = "+0.0"
                    else:
                        decimal_str = "-0.0"
                else:
                    decimal_str = f"{dec_value:.17g}"
                
                special_rows.append({
                    "Case": case_name,
                    "Type": dtype,
                    "Decimal": decimal_str,
                    "Sign": sign,
                    "Exponent": format_bits(exponent),
                    "Mantissa": format_bits(mantissa),
                    "Raw bits": format_bits(bits, 4)
                })
        except:
            # Some special values might not be supported in all formats
            special_rows.append({
                "Case": case_name,
                "Type": dtype,
                "Decimal": "Unsupported",
                "Sign": "-",
                "Exponent": "-", 
                "Mantissa": "-",
                "Raw bits": "-"
            })

if special_rows:
    st.subheader("Special Values Representation")
    st.table(special_rows)

st.markdown("""
**Key Observations:**
- **Zero**: Both +0.0 and -0.0 have all exponent and mantissa bits as 0, differing only in the sign bit
- **Infinity**: All exponent bits are 1, all mantissa bits are 0. Sign determines positive vs negative
- **NaN**: All exponent bits are 1, but at least one mantissa bit is 1. Different bit patterns can represent different NaN values
- **Subnormal Numbers**: When exponent is all 0s but mantissa is non-zero (not shown above), these represent very small numbers near zero

**Applications:**
- **Infinity**: Results from overflow or division by zero (1.0 / 0.0)
- **NaN**: Results from undefined operations (0.0 / 0.0, sqrt(-1), inf - inf)
- **Signed Zero**: Important in some mathematical contexts, like branch cuts in complex analysis
""")


st.markdown("---")
st.markdown("### 📚 References")
st.markdown("""
- [Brain Float Converter](https://flop.evanau.dev/brainfloat-converter)
- [Floating-Point Arithmetic: Issues and Limitations (Python Docs)](https://docs.python.org/3/tutorial/floatingpoint.html)
- [IEEE754 Tutorial: Creating the Bitstring for a Floating-Point Number](https://class.ece.iastate.edu/arun/Cpre305/ieee754/ie3.html#:~:text=For%20single%2Dprecision%20floating%2Dpoint,into%20the%20IEEE%20754%20string.)
- [IEEE 754 (Wikipedia)](https://en.wikipedia.org/wiki/IEEE_754#:~:text=%22Round%20to%20nearest%2C%20ties%20to,only%20required%20for%20decimal%20implementations.)
""")