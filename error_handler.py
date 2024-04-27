from flask import abort, Blueprint, jsonify

bp = Blueprint('error_handler', __name__)


def generate_error_response(exc: object):
    abort(exc.code, exc.__json__())


@bp.app_errorhandler(400)
def custom_400(response):
    return jsonify(response.description), 400


@bp.app_errorhandler(401)
def custom_401(response):
    return jsonify(response.description), 401


@bp.app_errorhandler(403)
def custom_403(response):
    return jsonify(response.description), 403


@bp.app_errorhandler(404)
def custom_403(response):
    return jsonify(response.description), 404


@bp.app_errorhandler(422)
def custom_422(response):
    return jsonify(response.description), 422


@bp.app_errorhandler(429)
def custom_429(response):
    return jsonify(response.description), 429


@bp.app_errorhandler(500)
def custom_500(response):
    return jsonify(response.description), 500


# -----------------------------------
# CustomError Class
# -----------------------------------

class CustomError(Exception):
    def __init__(self, message: str, code: int, instruction: str, traceback: str) -> None:
        self.message = message
        self.code = code
        self.instruction = instruction
        self.traceback = traceback

    def __json__(self) -> dict:
        response = {
            "code": self.code,
            "message": self.message,
            "instruction": self.instruction,
            "traceback": self.traceback
        }
        return response

    def __empty__(self) -> bool:
        if self.code == '' and self.message == '':
            return True
        else:
            return False
