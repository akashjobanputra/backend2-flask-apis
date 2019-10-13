from flask import jsonify, request
from ..models import Cluster
from .. import db
from . import api


@api.route('/clusters', defaults={'cluster_id': None})
@api.route('/clusters/<int:cluster_id>')
def get_clusters(cluster_id):
    if cluster_id:
        clusters = Cluster.query.filter_by(id=cluster_id).first_or_404()
        response = {
            'cluster': clusters.to_json()
        }
    else:
        clusters = Cluster.query.all()
        response = {
            'clusters': [cluster.to_json() for cluster in clusters]
        }
    return jsonify(response)


@api.route('/clusters', methods=['POST'])
def new_cluster():
    cluster = Cluster.from_json(request.json)
    db.session.add(cluster)
    db.session.commit()
    return jsonify(cluster.to_json()), 201
