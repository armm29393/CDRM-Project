from flask import Blueprint, send_from_directory, request
import os

react_bp = Blueprint('react_bp', __name__, static_folder=f'{os.getcwd()}/cdrm-frontend/dist', static_url_path='/')

@react_bp.route('/', methods=['GET'])
@react_bp.route('/<path:path>', methods=["GET"])
@react_bp.route('/<path>', methods=["GET"])
def index(path=''):
    if request.method == 'GET':
        if path != "" and os.path.exists(react_bp.static_folder + '/' + path):
            return send_from_directory(react_bp.static_folder, path)
        else:
            return send_from_directory(react_bp.static_folder, 'index.html')
    else:
        return
