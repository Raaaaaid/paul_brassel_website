
import os

from flask import render_template
from flask_httpauth import HTTPTokenAuth

from . import main
from .change_pepe import PepeImage


change_pepe_auth = HTTPTokenAuth()


@change_pepe_auth.verify_token
def verify_token(token):
    return token == os.environ['CHANGE_PEPE_TOKEN']


@main.route('/')
def index():
    return render_template('index.html', pepe_image=os.environ['PEPE_IMAGE'])


@main.route('/change_pepe/', methods=['POST'])
@change_pepe_auth.login_required
def change_pepe():
    info = {'before': os.environ['PEPE_IMAGE']}
    PepeImage.change()
    info['after'] = os.environ['PEPE_IMAGE']
    return info


@change_pepe_auth.error_handler
def change_pepe_auth_error(status):
    return 'Access denied!', status


@main.app_errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(_):
    return render_template('500.html'), 500
