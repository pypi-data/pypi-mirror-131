
from vsg.rules import split_line_at_token_when_between_tokens

from vsg import token

lTokens = []
lTokens.append(token.assertion.report_keyword)

oStart = token.assertion.keyword
oEnd = token.concurrent_assertion_statement.semicolon


class rule_002(split_line_at_token_when_between_tokens):
    '''
    Checks the report keyword is on it's own line for concurrent assertion statements.
    '''

    def __init__(self):
        split_line_at_token_when_between_tokens.__init__(self, 'assert', '002', lTokens, oStart, oEnd)
        self.solution = "Place **report** keyword on it's own line."
