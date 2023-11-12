from flask import Blueprint

subjectsHandled = Blueprint("subjectsHandled", __name__)

from . import controller
