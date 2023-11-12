from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import subject


@subject.route("/subjects")
def index():
    return render_template("subjectList.html")
