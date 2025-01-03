
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND AS ASC ASTERISK BY COMMA COUNT DATA DELETE DESC DOT EQUALS FILE FROM GREATER GROUP IDENTIFIER INNER INSERT INTO JOIN LESS LIMIT LPAREN NUMBER ON OR ORDER PATH RPAREN SELECT SEMICOLON SET STRING UPDATE VALUES WHEREstatement : SET DATA FROM FILE path eospath : PATHexpression : IDENTIFIER\n                     | IDENTIFIER DOT IDENTIFIER\n                     | ASTERISKstatement : SELECT columns FROM table_reference optional_clauses eosstatement : INSERT INTO table LPAREN columns RPAREN VALUES LPAREN values RPAREN eosstatement : UPDATE table SET column EQUALS value WHERE condition eosstatement : DELETE FROM table WHERE condition eosjoin_clause : INNER JOIN IDENTIFIER ON join_conditionjoin_condition : IDENTIFIER EQUALS IDENTIFIERaggregate_function : COUNT LPAREN expression RPAREN\n                              | COUNT LPAREN expression RPAREN AS IDENTIFIERtable_reference : IDENTIFIER\n                           | IDENTIFIER IDENTIFIER\n                           | table_reference join_clause\n                           | emptycolumns : columns COMMA column\n                   | ASTERISK\n                   | columncolumn : IDENTIFIER\n                  | IDENTIFIER DOT IDENTIFIER\n                  | aggregate_function\n                  | column AS IDENTIFIERtable : IDENTIFIEReos : SEMICOLONvalues : values COMMA value\n                  | valuevalue : NUMBER\n                 | STRINGcondition : column EQUALS value\n                     | LPAREN condition RPAREN\n                     | column LESS NUMBER\n                     | condition logical condition\n                     | column GREATER NUMBERwhere_clause : WHERE conditionlimit_clause : LIMIT NUMBERorder_clause : ORDER BY column\n                        | ORDER BY column DESC\n                        | ORDER BY column ASCgroup_columns : group_columns COMMA column\n                        | columngroup_clause : GROUP BY group_columnsempty :logical : AND\n                   | ORoptional_clauses : where_clause optional_clauses\n                            | order_clause optional_clauses\n                            | limit_clause optional_clauses\n                            | empty'
    
_lr_action_items = {'SET':([0,15,16,],[2,25,-25,]),'SELECT':([0,],[3,]),'INSERT':([0,],[4,]),'UPDATE':([0,],[5,]),'DELETE':([0,],[6,]),'$end':([1,60,61,62,76,103,108,],[0,-1,-26,-6,-9,-8,-7,]),'DATA':([2,],[7,]),'ASTERISK':([3,23,37,],[10,36,10,]),'IDENTIFIER':([3,5,14,17,19,20,21,22,23,25,29,37,39,49,54,59,66,68,70,77,78,79,88,94,104,],[11,16,16,16,29,11,32,33,35,11,52,11,11,11,71,11,84,11,86,11,-45,-46,11,99,107,]),'COUNT':([3,20,25,37,39,49,59,68,77,78,79,88,],[13,13,13,13,13,13,13,13,13,-45,-46,13,]),'INTO':([4,],[14,]),'FROM':([6,7,8,9,10,11,12,31,32,33,53,86,],[17,18,19,-20,-19,-21,-23,-18,-24,-22,-12,-13,]),'COMMA':([8,9,10,11,12,31,32,33,53,55,74,75,86,101,102,109,],[20,-20,-19,-21,-23,-18,-24,-22,-12,20,-29,-30,-13,106,-28,-27,]),'RPAREN':([9,10,11,12,31,32,33,34,35,36,53,55,71,74,75,83,86,89,90,91,92,93,101,102,109,],[-20,-19,-21,-23,-18,-24,-22,53,-3,-5,-12,72,-4,-29,-30,93,-13,-34,-31,-33,-35,-32,105,-28,-27,]),'AS':([9,11,12,31,32,33,38,53,58,85,86,],[21,-21,-23,21,-24,-22,21,70,21,21,-13,]),'EQUALS':([11,12,32,33,38,53,58,86,99,],[-21,-23,-24,-22,56,-12,80,-13,104,]),'LESS':([11,12,32,33,53,58,86,],[-21,-23,-24,-22,-12,81,-13,]),'GREATER':([11,12,32,33,53,58,86,],[-21,-23,-24,-22,-12,82,-13,]),'DESC':([11,12,32,33,53,85,86,],[-21,-23,-24,-22,-12,95,-13,]),'ASC':([11,12,32,33,53,85,86,],[-21,-23,-24,-22,-12,96,-13,]),'WHERE':([11,12,16,19,26,28,29,30,32,33,43,44,45,46,52,53,67,69,73,74,75,85,86,89,90,91,92,93,95,96,100,107,],[-21,-23,-25,-44,39,49,-14,-17,-24,-22,-16,49,49,49,-15,-12,-36,-37,88,-29,-30,-38,-13,-34,-31,-33,-35,-32,-39,-40,-10,-11,]),'ORDER':([11,12,19,28,29,30,32,33,43,44,45,46,52,53,67,69,74,75,85,86,89,90,91,92,93,95,96,100,107,],[-21,-23,-44,50,-14,-17,-24,-22,-16,50,50,50,-15,-12,-36,-37,-29,-30,-38,-13,-34,-31,-33,-35,-32,-39,-40,-10,-11,]),'LIMIT':([11,12,19,28,29,30,32,33,43,44,45,46,52,53,67,69,74,75,85,86,89,90,91,92,93,95,96,100,107,],[-21,-23,-44,51,-14,-17,-24,-22,-16,51,51,51,-15,-12,-36,-37,-29,-30,-38,-13,-34,-31,-33,-35,-32,-39,-40,-10,-11,]),'SEMICOLON':([11,12,19,28,29,30,32,33,40,41,42,43,44,45,46,47,52,53,57,63,64,65,67,69,74,75,85,86,89,90,91,92,93,95,96,98,100,105,107,],[-21,-23,-44,-44,-14,-17,-24,-22,61,-2,61,-16,-44,-44,-44,-50,-15,-12,61,-47,-48,-49,-36,-37,-29,-30,-38,-13,-34,-31,-33,-35,-32,-39,-40,61,-10,61,-11,]),'DOT':([11,35,],[22,54,]),'LPAREN':([13,16,24,39,49,59,77,78,79,87,88,],[23,-25,37,59,59,59,59,-45,-46,97,59,]),'FILE':([18,],[27,]),'INNER':([19,28,29,30,43,52,100,107,],[-44,48,-14,-17,-16,-15,-10,-11,]),'PATH':([27,],[41,]),'JOIN':([48,],[66,]),'BY':([50,],[68,]),'NUMBER':([51,56,80,81,82,97,106,],[69,74,74,91,92,74,74,]),'STRING':([56,80,97,106,],[75,75,75,75,]),'AND':([57,67,74,75,83,89,90,91,92,93,98,],[78,78,-29,-30,78,78,-31,-33,-35,-32,78,]),'OR':([57,67,74,75,83,89,90,91,92,93,98,],[79,79,-29,-30,79,79,-31,-33,-35,-32,79,]),'VALUES':([72,],[87,]),'ON':([84,],[94,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'columns':([3,37,],[8,55,]),'column':([3,20,25,37,39,49,59,68,77,88,],[9,31,38,9,58,58,58,85,58,58,]),'aggregate_function':([3,20,25,37,39,49,59,68,77,88,],[12,12,12,12,12,12,12,12,12,12,]),'table':([5,14,17,],[15,24,26,]),'table_reference':([19,],[28,]),'empty':([19,28,44,45,46,],[30,47,47,47,47,]),'expression':([23,],[34,]),'path':([27,],[40,]),'optional_clauses':([28,44,45,46,],[42,63,64,65,]),'join_clause':([28,],[43,]),'where_clause':([28,44,45,46,],[44,44,44,44,]),'order_clause':([28,44,45,46,],[45,45,45,45,]),'limit_clause':([28,44,45,46,],[46,46,46,46,]),'condition':([39,49,59,77,88,],[57,67,83,89,98,]),'eos':([40,42,57,98,105,],[60,62,76,103,108,]),'value':([56,80,97,106,],[73,90,102,109,]),'logical':([57,67,83,89,98,],[77,77,77,77,77,]),'join_condition':([94,],[100,]),'values':([97,],[101,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> SET DATA FROM FILE path eos','statement',6,'p_statement_set_data','parser.py',15),
  ('path -> PATH','path',1,'p_path','parser.py',18),
  ('expression -> IDENTIFIER','expression',1,'p_expression','parser.py',22),
  ('expression -> IDENTIFIER DOT IDENTIFIER','expression',3,'p_expression','parser.py',23),
  ('expression -> ASTERISK','expression',1,'p_expression','parser.py',24),
  ('statement -> SELECT columns FROM table_reference optional_clauses eos','statement',6,'p_statement_select','parser.py',31),
  ('statement -> INSERT INTO table LPAREN columns RPAREN VALUES LPAREN values RPAREN eos','statement',11,'p_statement_insert','parser.py',35),
  ('statement -> UPDATE table SET column EQUALS value WHERE condition eos','statement',9,'p_statement_update','parser.py',39),
  ('statement -> DELETE FROM table WHERE condition eos','statement',6,'p_statement_delete','parser.py',43),
  ('join_clause -> INNER JOIN IDENTIFIER ON join_condition','join_clause',5,'p_join_clause','parser.py',47),
  ('join_condition -> IDENTIFIER EQUALS IDENTIFIER','join_condition',3,'p_join_condition','parser.py',51),
  ('aggregate_function -> COUNT LPAREN expression RPAREN','aggregate_function',4,'p_aggregate_function','parser.py',55),
  ('aggregate_function -> COUNT LPAREN expression RPAREN AS IDENTIFIER','aggregate_function',6,'p_aggregate_function','parser.py',56),
  ('table_reference -> IDENTIFIER','table_reference',1,'p_table_reference','parser.py',63),
  ('table_reference -> IDENTIFIER IDENTIFIER','table_reference',2,'p_table_reference','parser.py',64),
  ('table_reference -> table_reference join_clause','table_reference',2,'p_table_reference','parser.py',65),
  ('table_reference -> empty','table_reference',1,'p_table_reference','parser.py',66),
  ('columns -> columns COMMA column','columns',3,'p_columns_list','parser.py',79),
  ('columns -> ASTERISK','columns',1,'p_columns_list','parser.py',80),
  ('columns -> column','columns',1,'p_columns_list','parser.py',81),
  ('column -> IDENTIFIER','column',1,'p_column','parser.py',88),
  ('column -> IDENTIFIER DOT IDENTIFIER','column',3,'p_column','parser.py',89),
  ('column -> aggregate_function','column',1,'p_column','parser.py',90),
  ('column -> column AS IDENTIFIER','column',3,'p_column','parser.py',91),
  ('table -> IDENTIFIER','table',1,'p_table','parser.py',107),
  ('eos -> SEMICOLON','eos',1,'p_eos','parser.py',111),
  ('values -> values COMMA value','values',3,'p_values_list','parser.py',115),
  ('values -> value','values',1,'p_values_list','parser.py',116),
  ('value -> NUMBER','value',1,'p_value','parser.py',120),
  ('value -> STRING','value',1,'p_value','parser.py',121),
  ('condition -> column EQUALS value','condition',3,'p_condition','parser.py',125),
  ('condition -> LPAREN condition RPAREN','condition',3,'p_condition','parser.py',126),
  ('condition -> column LESS NUMBER','condition',3,'p_condition','parser.py',127),
  ('condition -> condition logical condition','condition',3,'p_condition','parser.py',128),
  ('condition -> column GREATER NUMBER','condition',3,'p_condition','parser.py',129),
  ('where_clause -> WHERE condition','where_clause',2,'p_where_clause','parser.py',141),
  ('limit_clause -> LIMIT NUMBER','limit_clause',2,'p_limit_clause','parser.py',145),
  ('order_clause -> ORDER BY column','order_clause',3,'p_order_clause','parser.py',149),
  ('order_clause -> ORDER BY column DESC','order_clause',4,'p_order_clause','parser.py',150),
  ('order_clause -> ORDER BY column ASC','order_clause',4,'p_order_clause','parser.py',151),
  ('group_columns -> group_columns COMMA column','group_columns',3,'p_group_columns','parser.py',158),
  ('group_columns -> column','group_columns',1,'p_group_columns','parser.py',159),
  ('group_clause -> GROUP BY group_columns','group_clause',3,'p_group_clause','parser.py',166),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',170),
  ('logical -> AND','logical',1,'p_logical','parser.py',174),
  ('logical -> OR','logical',1,'p_logical','parser.py',175),
  ('optional_clauses -> where_clause optional_clauses','optional_clauses',2,'p_optional_clauses','parser.py',179),
  ('optional_clauses -> order_clause optional_clauses','optional_clauses',2,'p_optional_clauses','parser.py',180),
  ('optional_clauses -> limit_clause optional_clauses','optional_clauses',2,'p_optional_clauses','parser.py',181),
  ('optional_clauses -> empty','optional_clauses',1,'p_optional_clauses','parser.py',182),
]
