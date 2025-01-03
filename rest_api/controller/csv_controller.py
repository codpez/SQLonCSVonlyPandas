from werkzeug.utils import secure_filename

class CSVController:
    def __init__(self, csv_service, log_service):
        self.csv_service = csv_service
        self.log_service = log_service

    def handle_upload(self, file, request_info):
        """
        Maneja la subida de un archivo CSV.

        Args:
            file: Archivo subido.
            request_info: Información de la petición HTTP.

        Returns:
            tuple: (respuesta, código de estado).
        """
        try:
            # Validar que sea un archivo
            if not file:
                print("No se proporcionó un archivo")  # Debug
                return {"success": False, "message": "No se proporcionó archivo"}, 400

            # Validar que sea un CSV
            filename = secure_filename(file.filename)
            if not filename.endswith('.csv'):
                print(f"Formato incorrecto: {filename}")  # Debug
                return {"success": False, "message": "El archivo debe ser un CSV"}, 400

            # Procesar el CSV
            print(f"Procesando archivo: {filename}")  # Debug
            result = self.csv_service.upload_csv(file)

            # Registrar la acción
            print("Registrando log de subida")  # Debug
            self.log_service.log_request(
                url=request_info.get('url'),
                endpoint=request_info.get('endpoint'),
                method=request_info.get('method'),
                user_agent_string=request_info.get('user_agent'),
                ip_address=request_info.get('ip'),
                query=f"Upload CSV: {filename}"
            )

            if result["success"]:
                return result, 200
            else:
                return result, 400

        except Exception as e:
            print(f"Error al subir archivo: {str(e)}")  # Debugging
            return {"success": False, "message": f"Error interno: {str(e)}"}, 500


    def handle_download(self, request_info):
        """
        Maneja la descarga del CSV actual.

        Args:
            request_info: Información de la petición HTTP.

        Returns:
            tuple: (éxito, datos o mensaje de error).
        """
        try:
            success, data = self.csv_service.download_csv()

            # Registrar la acción
            self.log_service.log_request(
                url=request_info.get('url'),
                endpoint=request_info.get('endpoint'),
                method=request_info.get('method'),
                user_agent_string=request_info.get('user_agent'),
                ip_address=request_info.get('ip'),
                query="Download CSV"
            )

            if success:
                return success, data
            else:
                return {"success": False, "message": data}, 400

        except Exception as e:
            return {"success": False, "message": str(e)}, 500
