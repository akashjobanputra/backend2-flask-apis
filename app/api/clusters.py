from flask import jsonify, request
from ..models import Cluster
from .. import db
from . import api

@api.route('/clusters/')
def get_clusters():
    clusters = Cluster.query.all()
    return jsonify({
        'clusters': [cluster.to_json() for cluster in clusters]
    })

@api.route('/clusters/', methods=['POST'])
def new_cluster():
    cluster = Cluster.from_json(request.json)
    db.session.add(cluster)
    db.session.commit()
    return jsonify(cluster.to_json()), 201

