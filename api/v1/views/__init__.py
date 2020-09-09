#!/usr/bin/python3
"""Creating a flask app Blueprints
"""
from flask import Blueprint, request, abort, jsonify

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
