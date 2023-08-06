from setuptools import setup, find_packages

setup(
    name='pygments_w3c_ebnf',
    version='0.2',
    packages=find_packages(),
    description='A pygments lexer for the Extended Backus-Naur Format used by the W3C',
    url='https://github.com/rkaminsk/W3CEbnfLexer',
    author='William Heinbockel, Roland Kaminski',
    license='Apache 2.0',
    entry_points="""
[pygments.lexers]
w3c_ebnflexer = w3c_ebnflexer:W3CEbnfLexer
"""
)
