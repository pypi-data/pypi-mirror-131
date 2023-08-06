"""Tools for the serial number

This module provide functions to convert serial number between the 2
user format:
* String: 4 blocks of 4 digits each
* Big Integer
"""

# Author: Sébastien Gendre <sgendre@aquama.com>
# Copyright: Aquama 2021


def serial_number_old_to_new(serial_number: str,
                             prefix_chars: str = 'DCT',
                             prefix_number: int = 19) -> int:
    """Convert a serial number from old format to the new format

    Parameters:
    * serial_number: The serial number to convert
    * prefix_chars: The prefix chars to replace in the old format
    * prefix_number: The prefix number who will replace replace the
    prefix chars in the new format

    Return:
    * serial number in new format, int version
    """
    # Split the serial_number
    first_part, last_part = serial_number.split('/')

    # Convert the first part
    first_part = first_part.replace(
        prefix_chars,
        str(
            prefix_number
        ),
    )

    # Fill the last part to have a length of 12
    last_part = last_part.zfill(12)

    # Build the final version and return it
    return int(
        first_part + last_part
    )


def serial_number_int_to_string(serial_number: int,
                                block_size: int = 4,
                                block_separator: str = '-') -> str:
    """Convert a serial_number from int to string

    Parameter:
    * serial_number: The serial number to convert
    * block_size: The size of a block in the result
    * block_separator: The separator used between each block

    Return:
    * The serial_number in string version"""
    # Convert serial_number to string
    serial_number_string = str(serial_number)

    # Split to blocks
    blocks = []
    for block_start in range(0, len(serial_number_string), block_size):
        block_end = block_start + block_size
        blocks.append(
            serial_number_string[block_start:block_end]
        )

    # Join the blocks with the separator and return it
    return block_separator.join(blocks)    


def serial_number_string_to_int(serial_number: str,
                                block_size: int = 4,
                                block_separator: str = '-') -> int:
    """Convert a serial_number from string to int

    Parameter:
    * serial_number: The serial numer to convert

    Return:
    * The serial_number in int version"""
    # If the serial number is in old format
    if serial_number.startswith('DCT'):
        return serial_number_old_to_new(serial_number)
    
    # Separate the blocks
    blocks = serial_number.split(block_separator)
    normalized_blocks = []

    # For each block, fill it with zeros to make a block of length
    # `block_size`
    for block in blocks:
        normalized_blocks.append(
            block.zfill(block_size)
        )

    # Join the blocks and return it as int
    return int(''.join(normalized_blocks))
