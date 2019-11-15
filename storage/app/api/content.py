from flask import jsonify, request, g, url_for, current_app
import shelve
import os

from .error import build_error_message
from . import api


@api.route('/content/')
def get_all():
    with shelve.open(current_app.config['FLASK_DB']) as db:
        return jsonify({
            'content': db['content'],
            'count': len(db['content'])
        })


@api.route('/content/<int:content_id>')
def get_single(content_id):
    with shelve.open(current_app.config['FLASK_DB']) as db:
        try:
            return jsonify(db['content'][content_id])
        except IndexError:
            return jsonify("Content with {} index does not exist.".format(content_id)), 404


@api.route('/content/', methods=['POST'])
def add_new():
    with shelve.open(current_app.config['FLASK_DB']) as db:
        db['content'] += [request.json]
    return jsonify(request.json), 201
