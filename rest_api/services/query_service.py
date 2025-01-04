from sql.interpreter import SQLInterpreter  # Intérprete SQL personalizado
import pandas as pd
class QueryService:
    def __init__(self, csv_service):
        """
        Inicializa el servicio con una referencia al servicio CSV
        y una instancia del intérprete SQL.
        """
        self.csv_service = csv_service
        self.interpreter = SQLInterpreter()

    def execute_query(self, query):
        """
        Ejecuta una consulta SQL después de validarla con el intérprete.

        Args:
            query (str): Consulta SQL a ejecutar.

        Returns:
            tuple: (éxito, resultado o mensaje de error, tipo de operación)
        """
        try:
            # Validar y analizar la consulta SQL
            parsed = self.interpreter.interpret(query)
            print(f"Parsed query: {parsed}")
            if not parsed:
                return False, "Error al interpretar la consulta.", None
            
            command_type = parsed[0].upper()
            df = self.csv_service.csv_model.df

            if df is None:
                return False, "No hay datos cargados para ejecutar la consulta.", None

            # Procesar comandos SQL
            if command_type == "SELECT":
                return self._execute_select(parsed, df)
            elif command_type == "INSERT":
                return self._execute_insert(parsed, df)
            elif command_type == "UPDATE":
                return self._execute_update(parsed, df)
            elif command_type == "DELETE":
                return self._execute_delete(parsed, df)
            else:
                return False, f"Operación '{command_type}' no soportada.", None

        except Exception as e:
            return False, f"Error ejecutando la consulta: {str(e)}", None


    def _execute_select(self, parsed, df):
        """
        Ejecuta una operación SELECT en el DataFrame.

        Args:
            parsed: Consulta SQL interpretada.
            df: DataFrame con los datos actuales.

        Returns:
            tuple: (éxito, resultado, tipo de operación)
        """
        try:
            # Desempaquetar valores del query parseado
            _, columns, table, optional_clauses = parsed
            print(f"Parsed SELECT query: columns={columns}, table={table}, optional_clauses={optional_clauses}")

            # Seleccionar columnas específicas o todas (*)
            if columns == ['*']:
                selected_df = df
            else:
                selected_df = df[columns]

            optional_clauses = optional_clauses if isinstance(optional_clauses, dict) else {}
            # Aplicar cláusula WHERE
            where_clause = optional_clauses.get('WHERE')
            if where_clause:
                operator, condition_column, condition_value = where_clause

                # Validar que la columna exista en el DataFrame
                if condition_column not in df.columns:
                    return False, f"Error en SELECT: La columna '{condition_column}' no existe en la tabla.", "SELECT"

                # Generar la máscara booleana basada en el operador
                if operator == '=':
                    mask = df[condition_column] == condition_value
                elif operator == '>':
                    mask = df[condition_column] > condition_value
                elif operator == '<':
                    mask = df[condition_column] < condition_value
                else:
                    return False, f"Error en SELECT: Operador '{operator}' no soportado.", "SELECT"

                # Aplicar la máscara al DataFrame
                print(f"Aplicando WHERE: columna={condition_column}, operador={operator}, valor={condition_value}")
                selected_df = selected_df[mask]

            # Aplicar cláusula ORDER BY
            order_clause = optional_clauses.get('ORDER BY')
            if order_clause:
                order_column, order_direction = order_clause
                ascending = order_direction.upper() == 'ASC'
                selected_df = selected_df.sort_values(by=order_column, ascending=ascending)

            # Aplicar cláusula LIMIT
            limit_clause = optional_clauses.get('LIMIT')
            if limit_clause:
                selected_df = selected_df.head(limit_clause)

            # Convertir el DataFrame a lista de diccionarios para enviar al frontend
            result = selected_df.to_dict('records')

            return True, result, "SELECT"

        except Exception as e:
            return False, f"Error en SELECT: {str(e)}", "SELECT"



    def _execute_insert(self, parsed, df):
        """
        Ejecuta una operación INSERT en el DataFrame.

        Args:
            parsed: Consulta SQL interpretada.
            df: DataFrame con los datos actuales.

        Returns:
            tuple: (éxito, resultado, tipo de operación)
        """
        try:
            table, columns, values = parsed[1:]
            new_data = {col: [val] for col, val in zip(columns, values)}
            new_row = pd.DataFrame(new_data)
            updated_df = pd.concat([df, new_row], ignore_index=True)
            self.csv_service.update_csv(updated_df)

            return True, "Fila insertada correctamente.", "INSERT"
        except Exception as e:
            return False, f"Error en INSERT: {str(e)}", "INSERT"

    def _execute_update(self, parsed, df):
        """
        Ejecuta una operación UPDATE en el DataFrame.

        Args:
            parsed: Consulta SQL interpretada.
            df: DataFrame con los datos actuales.

        Returns:
            tuple: (éxito, resultado, tipo de operación)
        """
        try:
            table, column, new_value, condition = parsed[1:]
            operator, condition_column, condition_value = condition

            if operator == '=':
                condition_query = f"{condition_column} == @condition_value"
            elif operator == '>':
                condition_query = f"{condition_column} > @condition_value"
            elif operator == '<':
                condition_query = f"{condition_column} < @condition_value"
            else:
                return False, f"Error en UPDATE: Operador '{operator}' no soportado.", "UPDATE"


            matching_rows = df.query(condition_query).index
            if matching_rows.empty:
                return False, "No se encontraron filas que coincidan con la condición.", "UPDATE"

            df.loc[matching_rows, column] = new_value

            # Guardar el DataFrame actualizado en el CSV
            self.csv_service.update_csv(df)

            return True, "Filas actualizadas correctamente.", "UPDATE"
        except Exception as e:
            return False, f"Error en UPDATE: {str(e)}", "UPDATE"

    def _execute_delete(self, parsed, df):
        """
        Ejecuta una operación DELETE en el DataFrame.

        Args:
            parsed: Consulta SQL interpretada.
            df: DataFrame con los datos actuales.

        Returns:
            tuple: (éxito, resultado, tipo de operación)
        """
        try:
            table, conditions = parsed[1:]
            operator,condition_column, condition_value = conditions
            if operator == '=':
                condition_query = f"{condition_column} == @condition_value"
            elif operator == '>':
                condition_query = f"{condition_column} > @condition_value"
            elif operator == '<':
                condition_query = f"{condition_column} < @condition_value"
            else:
                return False, f"Error en DELETE: Operador '{operator}' no soportado.", "DELETE"

            # Obtener las filas que coinciden con la condición
            matching_rows = df.query(condition_query).index
            if matching_rows.empty:
                return False, "No se encontraron filas que coincidan con la condición.", "DELETE"

            # Eliminar las filas y actualizar el DataFrame
            updated_df = df.drop(matching_rows)
            self.csv_service.update_csv(updated_df)

            return True, "Filas eliminadas correctamente.", "DELETE"
        except Exception as e:
            return False, f"Error en DELETE: {str(e)}", "DELETE"
