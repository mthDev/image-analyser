import json

from auth_functions import decorators
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, session, url_for, redirect
from error_handler import bp as error_handler_bp
from image_analyser import analyse_image_api
from os import environ as env
from urllib.parse import urlencode

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

application = Flask(__name__)
application.register_blueprint(error_handler_bp)
application.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(application)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


@application.route('/', methods=['GET'])
@decorators.requires_auth
def index():
    return render_template(
        'index.html',
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@application.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@application.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@application.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("login", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID")
            }
        )
    )


@application.route('/image/analyse', methods=['POST'])
def image_analyser_api():
    output_format = request.args.get("output_format", default="JSON", type=str)
    response = analyse_image_api(request, output_format)
    return response


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=3000)
