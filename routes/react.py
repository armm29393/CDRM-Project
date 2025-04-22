from flask import Blueprint, send_from_directory
import os

react_bp = Blueprint('react_bp', __name__, static_folder=f'{os.getcwd()}/cdrm-frontend/dist', static_url_path='/')

@react_bp.route('/')
@react_bp.route('/<path:path>')
def index(path=''):
    if path != "" and os.path.exists(react_bp.static_folder + '/' + path):
        return send_from_directory(react_bp.static_folder, path)
    else:
        return send_from_directory(react_bp.static_folder, 'index.html')
