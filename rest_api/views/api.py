from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

class APIView:
    def __init__(self, csv_controller, query_controller, log_service):
        self.csv_controller = csv_controller
        self.query_controller = query_controller
        self.log_service = log_service

    def init_routes(self):
        @app.route('/csv/upload', methods=['POST'])
        def upload_csv():
            if 'file' not in request.files:
                return jsonify({"success": False, "message": "No se proporcionó archivo"}), 400
            
            file = request.files['file']
            request_info = {
                'url': request.url,
                'endpoint': request.endpoint,
                'method': request.method,
                'user_agent': request.headers.get('User-Agent'),
                'ip': request.remote_addr
            }

            response, status_code = self.csv_controller.handle_upload(file, request_info)
            return jsonify(response), status_code

        @app.route('/csv/download', methods=['GET'])
        def download_csv():
            request_info = {
                'url': request.url,
                'endpoint': request.endpoint,
                'method': request.method,
                'user_agent': request.headers.get('User-Agent'),
                'ip': request.remote_addr
            }

            success, data = self.csv_controller.handle_download(request_info)
            if success:
                return Response(
                    data,
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=data.csv'}
                )
            else:
                return jsonify({"success": False, "message": data}), 400

        @app.route('/query', methods=['POST'])
        def execute_query():
            request_info = {
                'url': request.url,
                'endpoint': request.endpoint,
                'method': request.method,
                'user_agent': request.headers.get('User-Agent'),
                'ip': request.remote_addr
            }

            query_data = request.get_json()
            response, status_code = self.query_controller.handle_query(query_data, request_info)
            return jsonify(response), status_code

        @app.route('/logs', methods=['GET'])
        def get_logs():
            try:
                success, logs = self.log_service.get_logs()
                if success:
                    return jsonify({"success": True, "data": logs}), 200
                else:
                    return jsonify({"success": False, "message": logs}), 400
            except Exception as e:
                return jsonify({"success": False, "message": str(e)}), 500

        print("Rutas inicializadas correctamente.")

