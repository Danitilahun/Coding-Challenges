def count_bytes_from_stream(stream):
    byte_count = 0
    try:
        while chunk := stream.read(8192):
            byte_count += len(chunk)
    except Exception as e:
        print(f"Error reading input for byte count: {e}")
        return -1
    return byte_count


def count_chars_from_stream(stream):
    try:
        content = stream.read()
        return len(content.decode('utf-8', errors='replace'))
    except Exception as e:
        print(f"Error reading input for character count: {e}")
        return -1


def count_words_and_lines_from_stream(stream):
    try:
        lines = stream.readlines()
        words = sum(len(line.split()) for line in lines)
        return len(lines), words
    except Exception as e:
        print(f"Error reading input for word/line count: {e}")
        return -1, -1
