
import json
import os

from flask import make_response, render_template
from flask_httpauth import HTTPTokenAuth
import requests

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
    if os.environ['FLASK_CONFIG'] == 'production':
        update_env_vars()

    response = make_response(info)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'

    return response


@change_pepe_auth.error_handler
def change_pepe_auth_error(status):
    return 'Access denied!', status


def update_env_vars():
    """
    Update the environment variable "PEPE_IMAGE" on render.com in case that the webservice
    is restarted. That prevents the current value of "PEPE_IMAGE" to get lost.
    """

    url = f'https://api.render.com/v1/services/{os.environ["RENDER_SERVICE_ID"]}/env-vars'
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': f'Bearer {os.environ["RENDER_API_KEY"]}',
    }
    response = requests.get(url, headers=headers)

    payload = []
    for d in json.loads(response.text):
        env_var = d['envVar']
        if env_var['key'] == 'PEPE_IMAGE':
            env_var['value'] = os.environ['PEPE_IMAGE']
        payload.append(env_var)
    requests.put(url, json=payload, headers=headers)


@main.app_errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(_):
    return render_template('500.html'), 500
