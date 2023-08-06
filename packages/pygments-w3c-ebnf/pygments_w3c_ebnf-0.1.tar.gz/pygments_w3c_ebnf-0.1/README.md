# W3C EBNF Lexer

A [pygments][] lexer for the Extended Backus-Naur Format ([EBNF][]) used
by the W3C.

An informal definition of the W3C EBNF format is available at
http://www.w3.org/TR/REC-xml/#sec-notation. Note that the W3C EBNF is
*not* the same as the ISO EBNF format defined in [ISO/IEC
14977:1996][ISO14977].

It can be used to produce the following

```w3c_ebnf
/* W3C EBNF description of the W3C EBNF grammar */
/* Source: http://railroad.my28msec.com */

Grammar              ::= Production*
Production           ::= NCName '::=' ( Choice | Link )
NCName               ::= /* [http://www.w3.org/TR/xml-names/#NT-NCName] */
Choice               ::= SequenceOrDifference ( '|' SequenceOrDifference )*
SequenceOrDifference ::= ( Item ( '-' Item | Item* ))?
Item                 ::= Primary ( '?' | '*' | '+' )?
Primary              ::= NCName | StringLiteral | CharCode | CharClass | '(' Choice ')'
StringLiteral        ::= '"' [^"]* '"' | "'" [^']* "'"
CharCode             ::= '#x' [0-9a-fA-F]+
CharClass            ::= '[' '^'? ( Char | CharCode | CharRange | CharCodeRange )+ ']'
Char                 ::= /* [http://www.w3.org/TR/xml#NT-Char] */
CharRange            ::= Char '-' ( Char - ']' )
CharCodeRange        ::= CharCode '-' CharCode
Whitespace           ::= S | Comment
S                    ::= #x9 | #xA | #xD | #x20
Comment              ::= '/*' ( [^*] | '*'+ [^*/] )* '*'* '*/'
```

## Install

First, ensure that both [setuptools][] and [pygments][] are installed.

Then,  install using `setuptools`. This will use setuptools entrypoint
to install the lexer and make it accessible from pygments

```
python setup.py
```

## Test

Now the lexer can be accessed via pygments.

`pygmentize` can be used to verify that the lexer was properly
installed. Since both W3C and ISO EBNF file formats use the `.ebnf`
extension, it is recommended to explicitly specify the W3C EBNF lexer
using the `-l w3c_ebnf` argument.

To run `pygmentize` on the provided w3c.ebnf grammar:

```
pygmentize -f html -l w3c_ebnf -O full w3c.ebnf > temp.html
```

and view the results in any browser.


# License

Copyright 2013 William Heinbockel

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


[pygments]: http://pygments.org/
[EBNF]: http://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_Form
[ISO14977]: http://www.iso.org/iso/catalogue_detail.htm?csnumber=26153
[setuptools]: https://pypi.python.org/pypi/setuptools
