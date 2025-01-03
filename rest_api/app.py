from models.csv_model import CSVModel
from models.request_log_model import RequestLogModel
from services.csv_service import CSVService
from services.query_service import QueryService
from services.log_service import LogService
from controller.csv_controller import CSVController
from controller.query_controller import QueryController
from views.api import APIView, app

def init_app():
    # Inicializar modelos
    csv_model = CSVModel()  # Modelo para manejar los datos en pandas
    log_model = RequestLogModel()  # Modelo para manejar los logs en SQLite
    log_model.initialize_db()
    # Inicializar servicios
    csv_service = CSVService(csv_model)  # Servicio para manejar los CSV
    query_service = QueryService(csv_service)  # Servicio para ejecutar queries SQL
    log_service = LogService(log_model)  # Servicio para registrar logs
    
    # Inicializar controladores
    csv_controller = CSVController(csv_service, log_service)
    query_controller = QueryController(query_service, log_service)
    
    # Inicializar API
    api = APIView(csv_controller, query_controller, log_service)
    api.init_routes()
    
    return app

if __name__ == '__main__':
    app = init_app()
    app.run(debug=True)
