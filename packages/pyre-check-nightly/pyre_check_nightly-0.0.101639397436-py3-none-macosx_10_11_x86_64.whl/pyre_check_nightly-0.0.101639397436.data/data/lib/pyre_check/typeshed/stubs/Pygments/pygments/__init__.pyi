from typing import Any

def lex(code, lexer): ...
def format(tokens, formatter, outfile: Any | None = ...): ...
def highlight(code, lexer, formatter, outfile: Any | None = ...): ...
