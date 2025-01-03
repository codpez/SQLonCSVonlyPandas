import ply.lex as lex

class SQLToken:
    """Represents a token with a type and value."""
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"SQLToken(type='{self.type}', value='{self.value}')"


class SQLLexer:
    """Lexical analyzer for tokenizing SQL statements."""

    # List of token names
    base_tokens=('IDENTIFIER', 'NUMBER','ASTERISK', 'STRING', 'PATH', 'EQUALS','COMMA', 'SEMICOLON',
        'LPAREN','RPAREN', 'GREATER','LESS','DOT')
    reserved = {
    'select' : 'SELECT',
    'from' : 'FROM',
    'where' : 'WHERE',
    'insert' : 'INSERT',
    'into': 'INTO',
    'values': 'VALUES',
    'update': 'UPDATE',
    'set' : 'SET',
    'delete' : 'DELETE',
    'and' : 'AND',
    'or' : 'OR',
    'data' : 'DATA',
    'file' : 'FILE',
    'limit': 'LIMIT',     
    'order': 'ORDER',     
    'by': 'BY',
    'group': 'GROUP',
    'inner': 'INNER',
    'join' : 'JOIN',
    'on' : 'ON',
    'count' : 'COUNT',
    'as' :  'AS',
    'desc' : 'DESC',
    'asc' : 'ASC'
    }
    def __init__(self):
        pass

    #Unifyied tokens and keywords   
    tokens = list(base_tokens) + list(reserved.values())
    # Define token patterns as class attributes
    t_ASTERISK = r'\*'
    t_SEMICOLON = r';'
    t_EQUALS = r'='
    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_GREATER = r'>'
    t_LESS = r'<'
    t_DOT = r'\.'

    # Define complex token patterns as methods
    
    def t_IDENTIFIER(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
         # Check for reserved words
        keyword=str(t.value).lower()
        if keyword in SQLLexer.reserved:
            t.type=SQLLexer.reserved.get(keyword)
        print(t.type)
        return t

    def t_NUMBER(self, t):
        r'\d*\.\d+|\d+'
        t.value = float(t.value) 
        return t

    def t_STRING(self, t):
        r"'[^']*'"
        t.value = t.value[1:-1]  # Remove quotes
        return t

    # Ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self):
        """Build the lexer using PLY's lex module."""
        self.lexer = lex.lex(module=self)

    def tokenize(self, sql_text):
        """Tokenize the input SQL text."""
        self.lexer.input(sql_text)
        tokens = []
        while tok := self.lexer.token():
            tokens.append(SQLToken(tok.type, tok.value))
        return tokens
