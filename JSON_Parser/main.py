JSON_TOKENS = {
    "{": "LEFT_BRACE",
    "}": "RIGHT_BRACE",
    "[": "LEFT_BRACKET",
    "]": "RIGHT_BRACKET",
    ",": "COMMA",
    ":": "COLON",
    "true": "BOOLEAN_TRUE",
    "false": "BOOLEAN_FALSE",
    "null": "NULL",
    "-?\\d+(\\.\\d+)?": "NUMBER",
    "\".*?\"": "STRING",
}

