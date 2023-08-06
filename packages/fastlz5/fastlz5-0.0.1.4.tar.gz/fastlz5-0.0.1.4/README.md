# FastLZ


Python wrapper for FastLZ_, a lightning-fast lossless compression library.

# Example:
from fastlz5 import compress, decompress
s = decompress(compress("hello there world", level=1))
assert(s == "hello there world")

# Example:


```
import os
import sys
import argparse

try:
    from fastlz5 import compress, decompress
except ModuleNotFoundError:
    sys.stderr.write(
        'fastlz lib not found, please install it with "python -m pip install fastlz5"')
    sys.exit(1)

# Breaks an array into chunks of n length each.
def chunks(l, n):    
    for i in range(0, len(l), n):
        yield l[i:i + n]

def bytes_to_c_array(bytes, variable_name):
    output_c_array = (
        "#include <stdint.h>\n" +
        f"extern const uint8_t {variable_name}[{len(bytes)}] = " + "{\n"
    )
    for byte_block in chunks(bytes, 64):
        output_c_array += '  '
        for byte in byte_block:
            output_c_array += f'{byte},'
        output_c_array += '\n'
    output_c_array += "};\n"
    return output_c_array

def main():
    parser = argparse.ArgumentParser(description='Prepare data file for teensy by compressing it and outputting a c-array')
    parser.add_argument('--input', help='Input file', required=True)
    parser.add_argument('--output', help='Output file, otherwise stream to stdout', required=False)
    parser.add_argument('--variable-name', help='Name for the variable of c_array', required=False)
    parser.add_argument('--no-compress', help='Disable FastLZ compression to file', action='store_true')

    args = parser.parse_args()
    if not os.path.exists(args.input):
        sys.stderr.write(f'File {args.input} does not exist.\n')
        sys.exit(1)

    with open(args.input, "rb") as fd:
        file_input_bytes = fd.read()

    if not args.no_compress:
        file_input_bytes = compress(file_input_bytes, level=1)

    var_name = args.variable_name or "data"
    output_c_array = bytes_to_c_array(file_input_bytes, var_name)

    if args.output:
        with open(args.output, "wt") as fd:
            fd.write(output_c_array)
    else:
        sys.stdout.write(f"{output_c_array}\n")

if __name__ == '__main__':
    main()
```