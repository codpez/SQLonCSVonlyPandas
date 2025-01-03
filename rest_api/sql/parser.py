import ply.yacc as yacc
from sql.lexer import SQLLexer

class SQLParser:
    """Parses SQL statements and produces a syntax tree."""

    def __init__(self):
        self.lexer = SQLLexer()
        self.lexer.build()
        self.tokens = SQLLexer.tokens
        self.parser = yacc.yacc(module=self)

    # Grammar rules for SQL statements
    def p_statement_set_data(self, p):
        """statement : SET DATA FROM FILE path eos"""

    def p_path(self, p):
        """path : PATH"""
        p[0]=p[1]

    def p_expression(self, p):
        """expression : IDENTIFIER
                     | IDENTIFIER DOT IDENTIFIER
                     | ASTERISK"""
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = { 'type': 'column', 'table': p[1],'column': p[3]}
    
    def p_statement_select(self, p):
        """statement : SELECT columns FROM table_reference optional_clauses eos"""
        p[0] = ("SELECT", p[2], p[4], p[5] or [])

    def p_statement_insert(self, p):
        "statement : INSERT INTO table LPAREN columns RPAREN VALUES LPAREN values RPAREN eos"
        p[0] = ("INSERT", p[3], p[5], p[9])

    def p_statement_update(self, p):
        "statement : UPDATE table SET column EQUALS value WHERE condition eos"
        p[0] = ("UPDATE", p[2], p[4], p[6], p[8])

    def p_statement_delete(self,p):
        "statement : DELETE FROM table WHERE condition eos"
        p[0] = ("DELETE",p[3],p[5])

    def p_join_clause(self,p):
        """join_clause : INNER JOIN IDENTIFIER ON join_condition"""
        p[0]= {'type': 'INNER JOIN','table':p[3], 'condition': p[5]}

    def p_join_condition(self,p):
        """join_condition : IDENTIFIER EQUALS IDENTIFIER"""
        p[0] = {'left' : p[1], 'operator' : p[2], 'right':p[3]}

    def p_aggregate_function(self,p): # para contar
        """aggregate_function : COUNT LPAREN expression RPAREN
                              | COUNT LPAREN expression RPAREN AS IDENTIFIER"""
        if len(p) == 5:
            p[0] = {'type': 'function', 'function': 'COUNT', 'args': p[3]}
        else:
            p[0] = {'type': 'function', 'function': 'COUNT', 'args': p[3], 'alias': p[6]}

    def p_table_reference(self,p):
        """table_reference : IDENTIFIER
                           | IDENTIFIER IDENTIFIER
                           | table_reference join_clause
                           | empty"""
        if len(p) == 2:
            if p[1] is None:  # caso empty
                p[0] = None
            else:
                p[0] = p[1]  # caso IDENTIFIER
        elif len(p) == 3:
            p[0] = {'table': p[1], 'alias': p[2]}  # caso con alias
        else:
            p[0] = {'base': p[1], 'join': p[2]}  # caso con join


    def p_columns_list(self, p):
        """columns : columns COMMA column
                   | ASTERISK
                   | column"""
        if len(p) == 2:
            p[0] = ["*"] if p[1] == "*" else [p[1]]  # Maneja tanto asterisco como column
        else:
            p[0] = p[1] + [p[3]] 

    def p_column(self, p):
        """column : IDENTIFIER
                  | IDENTIFIER DOT IDENTIFIER
                  | aggregate_function
                  | column AS IDENTIFIER""" # soporte para alias
        if len(p) == 2:
            p[0] = p[1] # common case
        elif len(p) == 4:
            if p[2] == 'AS':
                # Handle alias case
                p[0] = {'expr': p[1], 'alias': p[3]}
            else:
                # Handle table.column notation
                p[0] = {
                    'type': 'column',
                    'table': p[1],
                    'column': p[3]
                }

    def p_table(self, p):
        "table : IDENTIFIER"
        p[0] = p[1]

    def p_eos(self, p):
        """eos : SEMICOLON"""
        p[0] = p[1]

    def p_values_list(self, p):
        """values : values COMMA value
                  | value"""
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

    def p_value(self, p):
        """value : NUMBER
                 | STRING"""
        p[0] = p[1]

    def p_condition(self, p):
        """condition : column EQUALS value
                     | LPAREN condition RPAREN
                     | column LESS NUMBER
                     | condition logical condition
                     | column GREATER NUMBER"""
        if len(p) == 4 and p[1] == '(':
        # Extraemos la condición dentro de los paréntesis
            p[0] = p[2]
        elif len(p) == 4:
            # Condición con operador lógico
            p[0] = (p[2].lower(), p[1], p[3])
        else:
            # Condición simple
            p[0] = (p[2], p[1], p[3])

    def p_where_clause(self, p):
        """where_clause : WHERE condition"""
        p[0] = ("WHERE", p[2])

    def p_limit_clause(self, p):
        """limit_clause : LIMIT NUMBER"""
        p[0] = ("LIMIT", p[2])

    def p_order_clause(self, p):
        """order_clause : ORDER BY column
                        | ORDER BY column DESC
                        | ORDER BY column ASC"""
        if len(p) == 4:
            p[0] = ("ORDER", p[3])
        else:
            p[0] = ("ORDER", p[3], p[4])
        
    def p_group_columns(self, p):
        """group_columns : group_columns COMMA column
                        | column"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_group_clause(self, p):
        """group_clause : GROUP BY group_columns"""
        p[0] = ("GROUP", p[3])

    def p_empty(self, p):
        """empty :"""
        p[0] = None

    def p_logical(self, p):
        """logical : AND
                   | OR"""
        p[0] = p[1]

    def p_optional_clauses(self, p):
        """optional_clauses : where_clause group_clause order_clause limit_clause
                        | group_clause order_clause limit_clause
                        | where_clause order_clause limit_clause
                        | where_clause group_clause limit_clause
                        | where_clause group_clause order_clause
                        | where_clause limit_clause
                        | where_clause order_clause
                        | where_clause group_clause
                        | group_clause order_clause
                        | group_clause limit_clause
                        | order_clause limit_clause
                        | limit_clause
                        | group_clause
                        | order_clause
                        | where_clause
                        | empty"""
        p[0] = p[1]

    def p_error(self, p):
        if p:
            print(f"Syntax error at token {p.type}, value {p.value}, line {p.lineno}, position {p.lexpos}")
        else:
            print("Syntax error at EOF")

    def parse(self, sql_text):
        """Parse the input SQL text and return the parse tree."""
        return self.parser.parse(sql_text, lexer=self.lexer.lexer)
