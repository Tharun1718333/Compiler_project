import re



#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
PossibleOperatorsTokens   =  ['<=','>=','==','!=','&&','||']
PossibleDeclarationTokens =  ['int','string','float','boolean','void']
PossibleLoopTokens        =  ['while','for','main']
PossibleifelseTokens      =  ['if','else','elif']  
PossibleBreaks            =  [' ','\n','\t','#']
GivenVariables            =  []
ReturningVariable         =  ['void','return']
PossibleOutputTokens      =  ['printf','scanf','print','write','writeln']
#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_RFLOW    = 'RFLOW'
TT_LFLOW    = 'LFLOW'
TT_LSB      = 'LSB'
TT_RSB      = 'RSB'
TT_AMS      = 'AMS'
TT_LESS     = 'LESS'
TT_GREATER  = 'GREATER'
TT_NOT      = 'NOT'
TT_QMARK    = 'QMARK'
TT_AST      = 'AST'
TT_EQL      = 'EQL'
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        token_vals = []
        tokens_pos = []
        while self.current_char != None:
            if self.current_char in ' \t\n':
                self.advance()
            elif self.current_char in '#':
                self.advance()
                while self.current_char != '\n' :
                    self.advance()
            elif self.current_char in DIGITS:
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(self.make_number())
                token_vals.append(', ' + str(tokens[-1]))
            elif self.current_char == '+':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_PLUS))
                token_vals.append(', ' + '+')
                self.advance()
            elif self.current_char == '-':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_MINUS))
                token_vals.append('-')
                self.advance()
            elif self.current_char == '*':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_MUL))
                token_vals.append(', ' + '*')
                self.advance()
            elif self.current_char == '/':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_DIV))
                token_vals.append(', ' + '/')
                self.advance()
            elif self.current_char == '(':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_LPAREN))
                token_vals.append(', ' + '(')
                self.advance()
            elif self.current_char == ')':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_RPAREN))
                token_vals.append(', ' + ')')
                self.advance()
            elif self.current_char == '{':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_LFLOW))
                token_vals.append(', ' + '{')
                self.advance()
            elif self.current_char == '}':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_RFLOW))
                token_vals.append(', ' + '}')
                self.advance()
            elif self.current_char == '[':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_LSB))
                token_vals.append(', ' + '[')
                self.advance()
            elif self.current_char == ']':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_RSB))
                token_vals.append(', ' + ']')
                self.advance()
            elif self.current_char == '%':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_AMS))
                token_vals.append(', ' + '%')
                self.advance()
            elif self.current_char == '<':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_LESS))
                token_vals.append(', ' + '<')
                self.advance()
            elif self.current_char == '>':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_GREATER))
                token_vals.append(', ' + '>')
                self.advance()
            elif self.current_char == '!':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_NOT))
                token_vals.append(', ' + '!')
                self.advance()
            elif self.current_char == '?':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_QMARK))
                token_vals.append(', ' + '?')
                self.advance()
            elif self.current_char == ';':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_AST))
                token_vals.append(', ' + ';')
                self.advance()
            elif self.current_char == '=':
                tokens_pos.append(','+" Line number " + str(self.pos.ln))
                tokens.append(Token(TT_EQL))
                token_vals.append(', ' + '=')
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                temp_token = char
                if (temp_token == '''"''') or (temp_token == "'"):
                    while self.current_char != temp_token[0]:
                      temp_token += self.current_char
                      self.advance()  
                while (self.current_char != None) and not self.current_char in  ' \t\n,'  :
                    if self.current_char == None:
                        break
                    temp_token += self.current_char
                    self.advance()
                #print(GivenVariables)
                if temp_token in PossibleOperatorsTokens:
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("double operations")
                    token_vals.append(', ' + temp_token)
                elif temp_token in PossibleDeclarationTokens:
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("declaration tokens")
                    token_vals.append(', ' + temp_token)
                elif temp_token in PossibleLoopTokens:
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("PossibleLoopTokens")
                    token_vals.append(', ' + temp_token)
                elif temp_token in PossibleifelseTokens:
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("if else decalrators")
                    token_vals.append(', ' + temp_token)
                elif ((len(tokens) > 0) and (tokens[len(tokens)-1] == 'declaration tokens')):
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("variable")
                    token_vals.append(', ' + temp_token)
                    GivenVariables.append(temp_token)
                elif ((temp_token[0] == temp_token[-1] == "'") or (temp_token[0] == temp_token[-1] == '''"''')):
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("string")
                    token_vals.append(', ' + temp_token)
                elif temp_token in GivenVariables:
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("Previous variable")
                    token_vals.append(', ' + temp_token)
                elif temp_token in ReturningVariable:
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("Previous variable")
                    token_vals.append(', ' + temp_token)
                elif temp_token in PossibleOutputTokens:
                    tokens_pos.append(','+" Line number " + str(self.pos.ln))
                    tokens.append("Output Tokens")
                    token_vals.append(', ' + temp_token)
                else:
                    return [],[],[], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens,token_vals,tokens_pos, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens,tokens_vals,tokens_pos,error = lexer.make_tokens()
    if error:
     return None,None,None,error
    return tokens,tokens_vals,tokens_pos,None