"""pygments lexer for W3C EBNF grammars."""

from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import \
    Operator, String, Punctuation, Comment, Text, Literal, Name


class W3CEbnfLexer(RegexLexer):

    """
    Lexer for W3C EBNF grammars.

    Informal specification: <http://www.w3.org/TR/REC-xml/#sec-notation>.

    Based on the pygments EbnfLexer for the ISO14977:1996 EBNF Specification.

    """

    name = 'W3C EBNF'
    aliases = ['ebnf_w3c', 'w3c_ebnf']
    filenames = ['*.ebnf']
    mimetypes = ['text/x-w3c-ebnf']

    tokens = {
        'root': [
            include('whitespace'),
            include('comment_start'),
            include('identifier'),
            (r'::=', Operator, 'production'),
        ],
        'production': [
            (r'(?=[a-zA-Z][a-zA-Z0-9_\-]*\s*::=)', Text, '#pop'),
            (r'\n', Text.Break),
            include('whitespace'),
            include('comment_start'),
            include('identifier'),
            include('range_start'),
            include('codepoint'),
            (r'"[^"]*"', String.Double),
            (r"'[^']*'", String.Single),
            # (r'(\?[^?]*\?)', Name.Entity),
            (r'[()]', Punctuation),
            (r'[-|+*?]', Operator),
            # (r';', Punctuation, '#pop'),
        ],
        'range_start': [
            (r'(\[)(\^?)', bygroups(Punctuation, Operator), 'range'),
        ],
        'range': [
            include('codepoint'),
            include('escape'),
            (r'-', Operator),
            (r'\]', Punctuation, '#pop'),
            (r'.', Literal),
        ],
        'codepoint': [
            (r'#x[0-9a-fA-F]+', Literal),
        ],
        'escape': [
            (r'\\.', String.Escape)
        ],
        'whitespace': [
            (r'\s+', Text),
        ],
        'comment_start': [
            (r'\/\*', Comment.Multiline, 'comment'),
        ],
        'comment': [
            (r'[^*\/]', Comment.Multiline),
            include('comment_start'),
            (r'\*\/', Comment.Multiline, '#pop'),
            (r'[*\/]', Comment.Multiline),
        ],
        'identifier': [
            (r'([a-zA-Z][a-zA-Z0-9_\-]*)', Name),
        ],
    }
