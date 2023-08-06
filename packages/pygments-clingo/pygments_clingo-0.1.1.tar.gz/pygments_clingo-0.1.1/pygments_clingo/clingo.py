"""
    pygments_clingo.clingo
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Prolog and Prolog-like languages.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation

__all__ = ['ClingoLexer']


class ClingoLexer(RegexLexer):
    """
    Lexer for Clingo files.
    """
    name = 'Clingo'
    aliases = ['clingo']
    filenames = ['*.lp', '*.asp', '*.clingo', '*.gringo']
    mimetypes = ['text/plain']

    flags = re.UNICODE | re.MULTILINE

    tokens = {
        'root': [
            (r'%\*', Comment.Multiline, 'nested-comment'),
            (r'%.*', Comment.Single),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            (r'"(\\n|\\"|\\\\|[^\\])*"', String.Double),
            (r':-', Punctuation),
            (r'[\[\](){}]', Punctuation),
            (r'((?<!:):-|(?<!:):~|\.(?!\.)|,(?!;)|;(?!;)|:(?!:))', Punctuation),
            (r'\&[_]*[a-z][a-zA-Z_]*', Keyword),
            (r'[/<=>+\-*\\?&@|:;~k.!]+', Operator),
            (r'(#count|#sum|#show|#const|#edge|#minimize|#maximize|'
              '#defined|#heuristic|#project|#script|#program|'
              '#external|#theory|not)\b', Keyword),
            (r'(#inf|#sup|#true|#false)\b', Keyword.Constant),
            (r'[_]*[A-Z][a-zA-Z_]*', Name.Variable),
            (r'_', Name.Variable),
            (r'[_]*[a-z][a-zA-Z_]*', Text),
            (r'\s', Text),
        ],
        'nested-comment': [
            (r'\*%', Comment.Multiline, '#pop'),
            (r'%\*', Comment.Multiline, '#push'),
            (r'[^*%]+', Comment.Multiline),
            (r'[*%]', Comment.Multiline),
        ],
    }

    def analyse_text(text):
        return ':-' in text
