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
            (r'::=', Operator),
            (r'\n', Text.Break),
            include('whitespace'),
            (r'\/\*', Comment.Multiline, 'comment'),
            include('identifier'),
            include('range_start'),
            include('codepoint'),
            (r'"[^"]*"', String.Double),
            (r"'[^']*'", String.Single),
            (r'[()]', Punctuation),
            (r'[-|+*?]', Operator),
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
        'comment': [
            (r'\*\/', Comment.Multiline, '#pop'),
            (r'\/\*', Comment.Multiline, '#push'),
            (r'[^*\/]+', Comment.Multiline),
            (r'[*\/]', Comment.Multiline),
        ],
        'identifier': [
            (r'([a-zA-Z][a-zA-Z0-9_\-]*)', Name),
        ],
    }

    def get_tokens_unprocessed(self, text, stack=('root',)):
        '''
        This combines tokens of multi-line comments to avoid problems with
        latex's minted package.
        '''
        comment = None
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token == Comment.Multiline:
                if not comment:
                    comment = [index, token, value]
                else:
                    comment[2] += value
            else:
                if comment:
                    yield comment[0], comment[1], comment[2]
                    comment = None

                yield index, token, value

        if comment:
            yield comment[0], comment[1], comment[2]
            comment = None
