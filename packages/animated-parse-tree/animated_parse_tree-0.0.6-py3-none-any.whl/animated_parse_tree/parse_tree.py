from typing import Dict, List, Optional, Union, cast

from .utils.list_utils import find_element_where, index_first_element

from .utils.string_utils import simplify_expression
from .exceptions import LexingError, ParsingError, RegistrationError, TokenizationError
from .tree import Tree
from .default_bundles import *
from string import ascii_lowercase
from termcolor import colored
from copy import copy, deepcopy


class ParseTree(Tree):
    def __init__(self,
                 bundles: List[Bundle] = [
                     BASICS,
                     CONSTANTS,
                     EXPONENTIATION,
                     TRIGONOMETRY
                 ],
                 **kwargs):
        super().__init__(**kwargs)
        self.expression = ''
        self.token_lookup: Dict[str, Union[List[Operator], Operand]] = dict()
        for bundle in bundles:
            self.register(bundle=bundle)
        self.implicit_operator = Operator(
            symbol='*', func=lambda a, b: a * b, priority=5)

    def validate_registration(self, token):
        return
        # if len(token_obj) == 1:
        #     lexed_token = token_obj[0]
        # else:
        #     # Operator Overloaded
        #     if current_index == 0 or isinstance(lexed_token_list[-1], Operator) or lexed_token_list[-1] in '(,':
        #         lexed_token = find_element_where(
        #             token_obj, condition=lambda op: op.kind == 'pre')
        #     else:
        #         lexed_token = find_element_where(
        #             token_obj, condition=lambda op: op.kind == 'in')
        # if not isinstance(lexed_token, Operator):
        #     raise LexingError(
        #         f'Unknown token type {type(lexed_token)} encountered for {token}')
        # num_of_operands = lexed_token.operands
        # kind = lexed_token.kind
        # if type(num_of_operands) is not int or num_of_operands < 1:
        #     raise LexingError(
        #         f'Operator for {token} has invalid number of operands ({num_of_operands})')
        # if kind == 'post':
        #     if num_of_operands > 1:
        #         raise LexingError(
        #             'Post-fix only allowed for unary operators')
        #     lexed_token_list.append(lexed_token)
        # elif kind == 'in':
        #     if num_of_operands != 2:
        #         raise LexingError(
        #             'In-fix only allowed for binary operators')
        #     lexed_token_list.append(lexed_token)
        # elif kind == 'pre':
        #     if num_of_operands == 1:
        #         lexed_token_list.append(lexed_token)
        #     pass
        # else:
        #     raise LexingError(
        #         f'

    def register(self, bundle: Bundle) -> None:
        for op in bundle:
            if isinstance(op, Operand):
                self.token_lookup[op.symbol] = op
            elif isinstance(op, Operator):
                if op.symbol not in self.token_lookup:
                    self.token_lookup[op.symbol] = [op]
                elif isinstance(self.token_lookup[op.symbol], List):
                    cast(List[Operator],
                         self.token_lookup[op.symbol]).append(op)
            else:
                raise RegistrationError(
                    f'Unknown Operand/Operator encountered: {type(op)}')

    def lex_token(self, token: Optional[str] = None) -> Union[Operand, List[Operator]]:
        if token is not None:
            if token in self.token_lookup:
                if isinstance(self.token_lookup[token], List):
                    return cast(List[Operator], deepcopy(self.token_lookup[token]))
                else:
                    return cast(Operand, deepcopy(self.token_lookup[token]))
            raise LexingError(f'Unknown token {token} encountered')
        else:
            return [deepcopy(self.implicit_operator)]

    def read(self, expression: str) -> Tree:
        self.expression = expression
        return self

    # Tokenizer
    def tokenize(self, expression: str):
        token_list = []

        expression_simplified = simplify_expression(expression)

        # To check if single character is recognised
        digit_set = set('0123456789.')
        letter_set = set(ascii_lowercase)
        symbol_set = set(
            ''.join(filter(lambda s: not s.isalpha(), self.token_lookup.keys())))

        # To check if tokens are recognised
        recognised_tokens = set(self.token_lookup.keys()).union(set('(,)'))

        i = 0
        j = 1

        def slide_j(expression_simplified: str, current_set: set, j: int) -> int:
            while j < len(expression_simplified) and expression_simplified[j] in current_set:
                j += 1
            return j

        while j <= len(expression_simplified):
            char = expression_simplified[i]
            if char not in '(,)':
                if char in digit_set:
                    j = slide_j(expression_simplified,
                                current_set=digit_set, j=j)
                elif char in letter_set:
                    j = slide_j(expression_simplified,
                                current_set=letter_set, j=j)
                elif char in symbol_set:
                    j = slide_j(expression_simplified,
                                current_set=symbol_set, j=j)
                else:
                    raise TokenizationError(
                        expression_simplified=expression_simplified, kind='symbol', i=i, j=j)
            token = expression_simplified[i:j]
            if token in recognised_tokens or token[0] in digit_set:
                token_list.append(token)
            else:
                for k in range(j, i, -1):
                    token = expression_simplified[i:k]
                    if token in recognised_tokens:
                        token_list.append(token)
                        j = k
                        break
                else:
                    raise TokenizationError(
                        expression_simplified=expression_simplified, kind='token', i=i, j=j)
            i = j
            j += 1
        return token_list

    # Lexer

    def lex(self, tokens: List[str]):
        lexed_token_list: List = []

        digit_set = set('0123456789.')

        for token in tokens:
            if token in '(,)':
                lexed_token_list.append(token)
            elif token[0] in digit_set:
                # Normal numeric operand
                num = float(token) if '.' in token else int(token)
                lexed_token_list.append(Operand(value=num))
            else:
                token_obj = self.lex_token(token=token)
                if isinstance(token_obj, Operand):
                    lexed_token_list.append(self.lex_token(token=token))
                elif isinstance(token_obj, List):
                    if len(token_obj) == 1:
                        lexed_token_list.append(self.lex_token(token=token)[0])
                    else:
                        lexed_token_list.append(self.lex_token(token=token))
        return lexed_token_list

    # Parser

    def parse(self, token_obj_list: List, operand_expected: bool = True, index: int = 0, depth: int = 0):
        parsed_tokens = []
        while index < len(token_obj_list):
            token_obj = token_obj_list[index]
            if token_obj == ')':
                operand_expected = False
                if depth > 0:
                    return index, parsed_tokens
            elif token_obj == '(':
                if not operand_expected:
                    parsed_tokens.append(self.lex_token())
                terminating_index, nested_parsed_tokens = self.parse(
                    token_obj_list=token_obj_list, operand_expected=True, index=index + 1, depth=depth + 1)
                parsed_tokens.append(nested_parsed_tokens)
                index = terminating_index
            elif type(token_obj) is list:
                token_obj = find_element_where(
                    ls=token_obj, condition=lambda el: el.kind == 'pre' if operand_expected else el.kind != 'pre')
                operand_expected = self.insert_token_obj(parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
            else:
                operand_expected = self.insert_token_obj(parsed_tokens=parsed_tokens, token_obj=token_obj, operand_expected=operand_expected)
            index += 1
        return parsed_tokens

    def insert_token_obj(self, parsed_tokens: List[Union[Operand, Operator]], token_obj: Union[Operand, Operator], operand_expected: bool) -> bool:
        if operand_expected and isinstance(token_obj, Operand):
            parsed_tokens.append(token_obj)
            return False
        elif operand_expected and isinstance(token_obj, Operator) and token_obj.kind == 'pre':
            parsed_tokens.append(token_obj)
            return True
        elif (not operand_expected) and isinstance(token_obj, Operator) and token_obj.kind != 'pre':
            parsed_tokens.append(token_obj)
            return True
        elif (not operand_expected) and isinstance(token_obj, Operand):
            # Implicit Multiplication
            parsed_tokens.append(cast(Operator, self.lex_token()))
            parsed_tokens.append(token_obj)
            return False
        elif operand_expected and isinstance(token_obj, Operator) and token_obj.kind != 'pre':
            raise ParsingError(
                f'Expected operand but received non pre-fix operator {token_obj}')
        else:
            raise ParsingError('Unknown error encountered. Please check your expression again.')

    def build_sub_tree(self, token_obj_list: List, depth: int = 0):
        for token_obj in token_obj_list:
            if type(token_obj) is list:
                t = ParseTree()
                sub_root, _ = t.build_sub_tree(token_obj_list=token_obj)
                if sub_root is None:
                    raise ParsingError('Empty parenthesis encountered')
                tmptmp = ParseTree()
                tmptmp.root = sub_root
                self.insert(sub_root)
            else:
                self.insert(token_obj)
        return self.root, self.currentPointer

    def build(self):
        self.reset()
        tokens = self.tokenize(self.expression)
        lexed_tokens = self.lex(tokens)
        parsed_tokens = self.parse(lexed_tokens)
        self.build_sub_tree(parsed_tokens)

    def __str__(self) -> str:
        self()
        return super().__str__()

    def evaluate(self) -> Optional[Union[int, float]]:
        self()
        self.update(which='values')
        return self.root.value if self.root is not None else None

    def __call__(self):
        self.build()