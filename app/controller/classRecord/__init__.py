from flask import Blueprint

classRecord = Blueprint("classRecord", __name__)

from . import controller
