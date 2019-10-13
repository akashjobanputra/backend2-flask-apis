from flask import jsonify, request
from ..models import Tag, Machine
from .. import db
from . import api

@api.route('/tags/')
def get_tags():
    tags = Tag.query.all()
    return jsonify({
        'tags': [str(tag) for tag in tags]
    })
