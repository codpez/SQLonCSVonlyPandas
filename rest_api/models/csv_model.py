import pandas as pd
import os
class CSVModel:
    def __init__(self):
        """
        Modelo para manejar los datos del CSV en memoria usando pandas.
        """
        self.df= None
        self.columns = None
        self.filename = None
        self.total_rows = 0


    # En CSVModel
    def load_csv(self,file):
        """
        Carga el archivo CSV en un DataFrame.
        Y
        Extrae información básica: nombre del archivo, columnas, y número de filas.
        Args:
            file: Archivo CSV a cargar.
        """
        try:
            self.df = pd.read_csv(file)
            self.filename = file.filename
            self.columns = self.df.columns.tolist()
            self.total_rows = len(self.df)
            return {
                "success": True,
                "message": "Archivo CSV cargado exitosamente.",
                "metadata": {
                    "filename": self.filename,
                    "columns" : self.columns,
                    "total_rows": self.total_rows
                }
            }

        except Exception as e:
            return {"success": False, "message": f"Error al cargar el archivo: {str(e)}"}


        
    def get_data(self):
        """
        Retorna el DataFrame(CSV) actual en forma de diccionario.
        
        Returns:
            dict: Datos del CSV en memoria.
        """

        if self.df is not None:
            return self.df.to_dict('records')
        return None
    
    def save_csv(self):
        """Exporta el DataFrame actual como un string CSV
        
        Returns:
            str: Datos del CSV como string.

        """
        if self.df is not None:
                return self.df.to_csv(index=False)
        return None

    def update_data(self,new_df):
        """
        Actualiza el DataFrame con nuevos datos.
        
        Args:
            new_df: DataFrame actualizado.
        """
        self.df = new_df
        self.columns = new_df.columns.tolist()
        self.total_rows = len(new_df)