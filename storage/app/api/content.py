from flask import jsonify, request
from json import dumps, loads
from app.db import db
import shelve
import os
from . import api

@api.route('/content/')
def get_all():
    content = [loads(element) for element in db.lrange('content', 0, -1)]
    return jsonify({
        'content': content,
        'count': len(content)
    })


@api.route('/content/<int:content_id>')
def get_single(content_id):
    try:
        content = loads(*db.lrange('content', content_id, content_id))
    except TypeError:
        return jsonify("Content with {} index does not exist.".format(content_id)), 404
    return jsonify(content)


@api.route('/content/', methods=['POST'])
def add_new():
    db.lpush('content', request.json)
    return jsonify(request.json), 201
