import time

import connexion
import six
from werkzeug.exceptions import Unauthorized
import requests

from jose import JWTError, jwt

JWT_ISSUER = 'com.zalando.connexion'
JWT_SECRET = 'change_this'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'


def generate_token(user_id):
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        six.raise_from(Unauthorized, e)


def get_secret(user, token_info):
    return '''
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    '''.format(user=user, token_info=token_info)


def _current_timestamp():
    return int(time.time())

def get_token():
    # https://api.daf.teamdigitale.it/security-manager/v1/token
    print("token")
    header = connexion.request.headers['Authorization']
    url = "https://api.daf.teamdigitale.it/security-manager/v1/token"
    headers = {'authorization': header}
    response = requests.request("GET", url, headers=headers)
    print(response)
    print(response.text)
    print(response.encoding)
    return response.text

def basic_auth(username, password, required_scopes=None):
    print("ale")
    header = connexion.request.headers['Authorization']
    print(header)
    return  {'sub': 'user1', 'scope': ''}


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__)# specification_dir='openapi/', options={"swagger_ui": True})
    app.add_api('daf-openapi.yaml')
    app.run(port=8080)
