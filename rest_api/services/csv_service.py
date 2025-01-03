import pandas as pd
import os
from models.csv_model import CSVModel


class CSVService:
    def __init__(self, csv_model: CSVModel):
        self.csv_model = csv_model
        
    def upload_csv(self, file):
        """
        Carga un archivo CSV en el modelo.
        """
        print("Subiendo archivo CSV...")
        result = self.csv_model.load_csv(file)

        if not result['success']:
            print("Error al cargar CSV:", result['message'])  # Debugging
            return result

        print("Archivo CSV cargado exitosamente:", self.csv_model.df.head())  # Muestra las primeras filas
        return {
            "success": True,
            "message": result["message"],
            "metadata": result["metadata"],
            "preview": self.csv_model.df.head(3).to_dict('records')  # Previsualización
        }

        
    def download_csv(self):
        """
        Genera un CSV a partir de los datos actuales en el modelo.
        Returns:
            tuple: (éxito, datos o mensaje de error)
        """
        try:
            csv_data = self.csv_model.save_csv()
            if csv_data is None:
                return False, "No hay datos cargados para descargar."
            return True, csv_data
         
        except Exception as e:
            return False, f"Error generando CSV: {str(e)}"
        
    def update_csv(self, new_data):
        """
        Actualiza el DataFrame con nuevos datos.

        Args:
            new_data: DataFrame o datos a actualizar.

        Returns:
            dict: Resultado de la operación.
        """
        try:
            if isinstance(new_data, pd.DataFrame):
                self.csv_model.update_data(new_data)
            else:
                new_df = pd.DataFrame(new_data)
                self.csv_model.update_data(new_df)
            return {"success": True, "message": "Datos actualizados correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error actualizando datos: {str(e)}"}