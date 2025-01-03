class QueryController:
    def __init__(self, query_service, log_service):
        self.query_service = query_service
        self.log_service = log_service

    def handle_query(self, query_data, request_info):
        """
        Maneja la ejecución de queries SQL.

        Args:
            query_data: dict con el query SQL.
            request_info: dict con información de la petición HTTP.

        Returns:
            tuple: (respuesta, código de estado).
        """
        try:
            # Validar que venga el query
            if not query_data or 'query' not in query_data:
                return {"success": False, "message": "No se proporcionó query SQL"}, 400

            query = query_data['query']

            # Ejecutar el query
            success, result, operation = self.query_service.execute_query(query)

            # Registrar el query en los logs
            self.log_service.log_request(
                url=request_info.get('url'),
                endpoint=request_info.get('endpoint'),
                method=request_info.get('method'),
                user_agent_string=request_info.get('user_agent'),
                ip_address=request_info.get('ip'),
                query=query
            )

            if success:
                return {
                    "success": True,
                    "operation": operation,
                    "data": result,
                    "message": "Query ejecutado exitosamente."
                }, 200
            else:
                # Asegúrate de que el `result` sea siempre un mensaje claro en caso de error
                error_message = result if isinstance(result, str) else "Error desconocido al ejecutar el query."
                return {
                    "success": success,
                    "message": error_message,
                    "data": result,
                    "operation": operation
                }, 400


        except Exception as e:
            return {
                "success": False,
                "message": f"Error ejecutando query: {str(e)}",
                "data": result,
                "operation": operation
            }, 500
