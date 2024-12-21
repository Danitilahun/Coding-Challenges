from enum import IntEnum
class ControlChars(IntEnum):
    """
    Represents ASCII character codes with descriptive names used in the NATS protocol.

    Usage:
        These character codes are used for parsing and interpreting commands
        in the incoming byte stream.
        
    Example:
        - ControlChars.CARRIAGE_RETURN: Represents the carriage return character (`\r`).
        - ControlChars.LINE_FEED: Represents the line feed character (`\n`).
    """
    CARRIAGE_RETURN = ord('\r')  # Carriage Return (CR)
    LINE_FEED = ord('\n')        # Line Feed (LF)
    SPACE = ord(' ')             # Space character
    TAB = ord('\t')              # Tab character
    UPPERCASE_C = ord('C')       # 'C' character (uppercase)
    LOWERCASE_C = ord('c')       # 'c' character (lowercase)
    UPPERCASE_O = ord('O')       # 'O' character (uppercase)
    LOWERCASE_O = ord('o')       # 'o' character (lowercase)
    UPPERCASE_N = ord('N')       # 'N' character (uppercase)
    LOWERCASE_N = ord('n')       # 'n' character (lowercase)
    UPPERCASE_E = ord('E')       # 'E' character (uppercase)
    LOWERCASE_E = ord('e')       # 'e' character (lowercase)
    UPPERCASE_T = ord('T')       # 'T' character (uppercase)
    LOWERCASE_T = ord('t')       # 't' character (lowercase)
    UPPERCASE_P = ord('P')       # 'P' character (uppercase)
    LOWERCASE_P = ord('p')       # 'p' character (lowercase)
    UPPERCASE_I = ord('I')       # 'I' character (uppercase)
    LOWERCASE_I = ord('i')       # 'i' character (lowercase)
    UPPERCASE_G = ord('G')       # 'G' character (uppercase)
    LOWERCASE_G = ord('g')       # 'g' character (lowercase)
    UPPERCASE_S = ord('S')       # 'S' character (uppercase)
    LOWERCASE_S = ord('s')       # 's' character (lowercase)
    UPPERCASE_U = ord('U')       # 'U' character (uppercase)
    LOWERCASE_U = ord('u')       # 'u' character (lowercase)
    UPPERCASE_B = ord('B')       # 'B' character (uppercase)
    LOWERCASE_B = ord('b')       # 'b' character (lowercase)
