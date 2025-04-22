from custom_functions.prechecks.precheck import run_precheck
run_precheck()
from flask import Flask
from flask_cors import CORS
from routes.react import react_bp
from routes.api import api_bp
from routes.remote_device_wv import remotecdm_wv_bp

app = Flask(__name__)

CORS(app)

# Register the blueprint
app.register_blueprint(react_bp)
app.register_blueprint(api_bp)
app.register_blueprint(remotecdm_wv_bp)

if __name__ == '__main__':
    app.run(debug=True)