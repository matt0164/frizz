from waitress import serve
from local_web_app import app

serve(app, host='0.0.0.0', port=8000)
