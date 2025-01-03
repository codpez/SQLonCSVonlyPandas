from sql.parser import SQLParser

class SQLInterpreter:
    """SQL Interpreter that uses SQLLexer and SQLParser to interpret SQL statements."""

    def __init__(self):
        self.parser = SQLParser()

    def interpret(self, sql_text):
        """Interpret the SQL statement."""
        parse_tree = self.parser.parse(sql_text)
        return parse_tree
